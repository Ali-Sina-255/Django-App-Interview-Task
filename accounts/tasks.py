from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
        message='',  # No plain text message
        from_email=None,  # Use default from email in settings
        recipient_list=[user.email],  # List of recipients
        html_message=message  # HTML content of the email
    )
    

@shared_task
def send_verification_email_task(user_id, email_subject, email_template, domain):
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    
    message = render_to_string(email_template, {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    
    to_email = user.email
    mail = EmailMessage(
        subject=email_subject,
        body=message,
        from_email=None,  # Optional: set a default from email
        to=[to_email]
    )
    mail.content_subtype = 'html'  # Send as HTML
    mail.send()