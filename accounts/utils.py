from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage



def send_verification_email(request, user, email_subject,email_template):
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user':user,
        "domain":current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(email_subject,message,to=[to_email])
    mail.content_subtype = 'html'
    mail.send()
    
    


def send_otp_verification_email(request, user, email_subject, email_template, otp):
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'otp': otp  # Pass the OTP to the template context
    })
    
    to_email = user.email
    mail = EmailMessage(email_subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()
    


def send_reset_password_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Reset your password '
    message = render_to_string('accounts/email/reset_password_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(email_subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()