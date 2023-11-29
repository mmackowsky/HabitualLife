from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.tokens import account_activation_token
import logging
from django.contrib.auth.models import User


@shared_task
def send_email(user_pk, to_email):
    user = User.objects.get(pk=user_pk)
    current_site = Site.objects.get_current()
    mail_subject = "Activation link has been sent to your email id"
    message = render_to_string(
        "users/acc_active_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    logging.debug("Email sent in activation case.")
