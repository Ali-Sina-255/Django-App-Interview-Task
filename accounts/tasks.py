from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from . utils import send_verification_email

from api.models import Command
import subprocess

@shared_task
def send_otp_verification_email_task(user_id, email_subject, email_template, otp, domain):
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    # Prepare the email message
    context = {
        'user': user,
        'otp': otp,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)
    
    # Send the email
    send_mail(
        subject=email_subject,
        message='',  
        from_email=None,  
        recipient_list=[user.email],
        html_message=message 
    )
    

@shared_task
def send_verification_email_task(user_id, email_subject, email_template, host):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    
    # Create request object with host for sending email
    class DummyRequest:
        def __init__(self, host):
            self.get_host = lambda: host
            
    request = DummyRequest(host)
    
    send_verification_email(request, user, email_subject, email_template)

@shared_task
def execute_command_task(command_id):
    try:
        command = Command.objects.get(pk=command_id)
        
        result = subprocess.run(command.body, shell=True, capture_output=True, text=True)
      
        job = command.job
        if result.returncode == 0:
            job.status = 'completed'
            job.result = result.stdout
        else:
            job.status = 'failed'
            job.result = result.stderr
        job.save()

    except Command.DoesNotExist:
        print("Command not found.")
    except Exception as e:

        print(f"An error occurred while executing the command: {e}")



@shared_task
def send_reset_password_email_task(domain, user_id, token):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    email_subject = 'Reset your password'
    message = render_to_string('accounts/email/reset_password_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    to_email = user.email
    mail = EmailMessage(email_subject, message, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()