from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
# Create your models here.
class Book(models.Model):
    id=models.IntegerField(primary_key=True)
    section=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    nfp=models.IntegerField()
    # cat=models.CharField(max_length=50,null=True,editable=True,blank=True)
    cat=models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name
     
    @property 
    def check_cat(self):
        if self.nfp>500:
            val='reference book'
        else:
            val='text book'

        return val

    def save(self,*args,**kwargs):
        self.cat=self.check_cat
        super(Book, self).save(*args,**kwargs)


class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should habe a Email')
        
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError('Password should not be none')
        if email is None:
            raise TypeError('Users should habe a Email')
        
        user = self.create_user(username, email, password)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True #if is_active=False deactives the account (wont be able to access it using the admin panel)
        user.save()
        return user 

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=100,unique=True)
    email=models.CharField(max_length=150,unique=True)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        return ''

    
