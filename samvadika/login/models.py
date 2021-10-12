from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_active', True)
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    image=models.ImageField(null=True, blank= True, default="pic.jpeg")
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name



class Question(models.Model):
    question = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    tag1 = models.CharField(max_length=15)
    tag2 = models.CharField(max_length=15)
    tag3 = models.CharField(max_length=15)
    tag4 = models.CharField(max_length=15)
    tag5 = models.CharField(max_length=15)
    tag6 = models.CharField(max_length=15)
    tag7 = models.CharField(max_length=15)
    tag8 = models.CharField(max_length=15)
    tag9 = models.CharField(max_length=15)
    tag10 = models.CharField(max_length=15)
    threadid = models.AutoField(primary_key=True)
  
class Reply(models.Model):
    threadid =  models.ForeignKey(Question, on_delete=models.CASCADE)
    reply_date = models.DateTimeField(default=timezone.now)
    reply=models.CharField(max_length=1000)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)

