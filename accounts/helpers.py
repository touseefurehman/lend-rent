

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import threading


def send_forget_password_mail(request, email, token):
    subject = 'Your forget password link'
    domain_name = get_current_site(request)
    domain = str(domain_name)
    message = f'Hi , click on the link to reset your password {domain}/accounts/resetPassword/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


class EmailThread(threading.Thread):

    def __init__(self, request, email, token):
        self.request = request
        self.email = email
        self.token = token
        threading.Thread.__init__(self)

    def run(self):
        subject = 'Your forget password link'
        domain_name = get_current_site(self.request)
        domain = str(domain_name)
        message = f'Hi , click on the link to reset your password {domain}/accounts/resetPassword/{self.token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email]
        send_mail(subject, message, email_from, recipient_list)
