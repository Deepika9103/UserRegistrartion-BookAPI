#from django.core.mail import send_email
from django.conf import settings
from django.core import mail 

class Util:
    @staticmethod
    def send_email(data):
        # email=mail.EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['to_email']])
        # email.fail_silently=False
        # email.send()

        email=mail.EmailMessage(
            data['email_subject'],
            data['email_body'],
            settings.EMAIL_HOST_USER,
            [data['to_email']])
        email.fail_silently=False
        email.send()

        # mail.send_mail(
        #     data['email_subject'],
        #     data['email_body'],
        #     'muchhaladeepika@gmail.com',
        #     [data['to_email']],
        #     fail_silently=False,
        # )
        