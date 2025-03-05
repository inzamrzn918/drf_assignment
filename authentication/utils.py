import traceback
from idlelib.pyparse import trans

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings


def send_otp_email(email, otp):
    """Send OTP via HTML email"""
    subject = 'Your OTP Code'
    try:
        # Render HTML email template
        html_content = render_to_string('emails/otp_ui.html', {'otp': otp})

        # Create email message
        email_message = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
    except Exception as e:
        traceback.print_exc()
        print(e)