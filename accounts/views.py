from datetime import datetime
import pyotp

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

from .forms import UserRegistrationForm
from .tasks import send_verification_email_task, send_otp_verification_email_task
from .utils import send_verification_email, send_otp_verification_email, send_reset_password_email
from .helper import send_otp
from accounts.models import User


def home_view(request):
    return render(request, 'accounts/home.html')


def user_registration(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered")
        return redirect("home")
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
    
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            # Send verification email asynchronously using Celery
            mail_subject = "Please Activate your Registration"
            email_template = "accounts/email/verification_email.html"
            send_verification_email_task.delay(
                user.pk, mail_subject, email_template, request.get_host()
            )

            messages.success(request, "Your registration was successful. Please check your email to activate your account.")
            return redirect("login-user")
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, "Congratulations, your account is activated.")
        return redirect("login-user")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("register_user")


def login_view(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            otp = send_otp(request)
            email_subject = 'Your OTP Code'
            email_template = "accounts/email/otp_email.html"
            send_otp_verification_email_task.delay(
                user_id=user.id,
                email_subject=email_subject,
                email_template=email_template,
                otp=otp,
                domain=get_current_site(request).domain
            )
            request.session['email'] = email
            return redirect('otp')
        else:
            error_message = 'Invalid username and password'
    
    context = {
        'error_message': error_message,
    }
    return render(request, 'accounts/login.html', context)


def otp_views(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        
        if otp_secret_key and otp_valid_date:
            try:
                valid_date = datetime.fromisoformat(otp_valid_date)
                
                if valid_date > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(otp):
                        try:
                            user = User.objects.get(email=email)
                            login(request, user)
                           
                            del request.session['otp_secret_key']
                            del request.session['otp_valid_date']
                            return redirect('home')
                        except User.DoesNotExist:
                            error_message = "No user found with the provided email address."
                    else:
                        error_message = 'Invalid one-time password.'
                else:
                    error_message = "One-time password has expired!"
            except ValueError:
                error_message = "Invalid OTP valid date format!"
        else:
            error_message = "Oops, something went wrong!"

    context = {'error_message': error_message}
    return render(request, 'accounts/otp.html', context)


def logout_view(request):
    logout(request)
    return redirect('login-user')

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)
            mail_subject = "Reset your password"
            email_template = "accounts/email/reset_password_email.html"
            send_verification_email_task.delay(
                user.pk, mail_subject, email_template, request.get_host()
            )
            send_reset_password_email(request, user)
            messages.success(request, "Your password reset link has been sent to your email address.")
            return redirect("login-user")
        else:
            messages.error(request, "Account does not exist.")
            return redirect("forgot_password")

    return render(request, "accounts/forgot_password.html")



def reset_password_validate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password.")
        return redirect("reset_password")
    else:
        messages.error(request, "This link has expired.")
        return redirect("login-user")


def reset_password_view(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect("login-user")
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")
    return render(request, "accounts/reset_password.html")


def my_account(request):
    return render(request, 'accounts/my_account.html')
