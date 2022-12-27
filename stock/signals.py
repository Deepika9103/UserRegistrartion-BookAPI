from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_init,pre_save,pre_delete,post_init,post_save,post_delete
from .models import Book
from rest_framework.authtoken.models import Token
from django.conf import settings

def login_success(sender,request, user, **kwargs):
    print("Logged-in signal")
    print("Sender:",sender)
    print("Request:",request)
    print("User Password:", user.password)
    print(f'kwargs: {kwargs}')
user_logged_in.connect(login_success,sender=User)

@receiver(user_logged_out,sender=User)
def logout_success(sender,request, user, **kwargs):
    print("Logged-out signal")
    print("Sender:",sender)
    print("Request:",request)
    print("User Email:", user.email)
    print(f'kwargs: {kwargs}')

@receiver(user_login_failed)
def login_failed(sender,request,credentials,**kwargs):
    print("Login failed signal")
    print("Sender:",sender)
    print("Credentials:",credentials)
    print("Request:",request)
    print(f'kwargs: {kwargs}')

@receiver(pre_save, sender=Book)
def at_beginning_save(sender,instance,**kwargs):
    print("Pre_save method")

# @receiver(post_save,sender=Book)
# def at_end_save(sender,instance,created,**kwargs):
#     if created:
#         print("Post_save method")
#         print("New record created")
#         print("Created:",created)
#     else:
#         print("Old record updated")
#         print("Created:",created)


#this signal creates signals
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(pre_delete,sender=Book)
def at_beginning_delete(sender,instance,**kwargs):
    print("Pre_delete method")
    print("Instance:",instance)

@receiver(pre_delete,sender=Book)
def at_end_delete(sender,instance,**kwargs):
    print("Post_delete method")
    print("Instance:",instance)

@receiver(pre_init,sender=Book)
def at_beginning_init(sender,*args,**kwargs):
    print("Pre init signal")

@receiver(post_init,sender=Book)
def at_end_init(sender,*args,**kwargs):
    print("Post init signal")


