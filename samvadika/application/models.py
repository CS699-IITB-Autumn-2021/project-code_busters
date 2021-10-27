from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User





class CustomAccountManager(BaseUserManager):
    """CustomAccountManager class extends BaseUserManager providing two additional methods create_superuser and create_user to create the superuser and user as without superuser we are unable to access the admin.
    :param BaseUserManager: models.BaseUserManager class act as a superclass for CustomAccountManager class.
    :type BaseUserManager: class
    """
    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

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
    """Custom user model extends models.AbstractBaseUser class which provide the core implementation of user model and models.PermissionMixin class which provide 
     all the methods and database fields necessary to support Django’s permission model.
    
    :param AbstractBaseUser: models.AbstractBaseUser class act as a superclass for NewUser model.
    :type AbstractBaseUser: class
    :param PermissionMixin: models.PermissionMixin class inherited by NewUser model.
    :type PermissionMixin: class
    """
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=150, blank=True)
    image=models.ImageField(null=True, blank= True, default="pic.jpeg")
    start_date = models.DateTimeField(default=timezone.now)
    
    interest_form_submitted = models.BooleanField(default=False)
    fb_link = models.URLField(max_length=200, default="https://www.facebook.com/")
    linkedin_link = models.URLField(max_length=200, default="https://www.linkedin.com/in/")

    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    score=models.IntegerField(default=5)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        """Return user name"""
        return self.user_name

class Hobby(models.Model):
    """Model Hobby extends django.db.models.Model inbuilt class for storing hobbies of the user with user instance in many to one form.
    :param model.Model: django.db.models.Model class act as a superclass for the Hobby model.
    :type models.Model: class
    """
    hobby_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)



class Question(models.Model):
    """Model Question extends django.db.models.Model inbuilt class for storing question with published date, thread id and user who post the question.
    :param model.Model: django.db.models.Model class act as a superclass for the Question model.
    :type models.Model: class
    """
    question = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    #tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    threadid = models.AutoField(primary_key=True)

class Tag(models.Model):
    """Model Tag extends django.db.models.Model inbuilt class for storing tag of the question with question instance.
    :param model.Model: django.db.models.Model class act as a superclass for the Tag model.
    :type models.Model: class
    """
    tag_name = models.CharField(max_length=50,default=" ", blank=True, null=True)
    threadid=models.ForeignKey(Question, on_delete=models.CASCADE)

class Reply(models.Model):
    """Model Reply extends django.db.models.Model inbuilt class for storing reply to the question with reply date, reply id, number of upvotes, number of downvotes, corresponding question instance and user who replied.
    :param model.Model: django.db.models.Model class act as a superclass for the Reply model.
    :type models.Model: class
    """
    threadid =  models.ForeignKey(Question, on_delete=models.CASCADE)
    reply_date = models.DateTimeField(default=timezone.now)
    reply=models.CharField(max_length=1000)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    replyid = models.AutoField(primary_key=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

class Save(models.Model):
    threadid =  models.ForeignKey(Question, on_delete=models.CASCADE)  
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    class Meta:
        unique_together=[[ 'threadid','user_name']]
   

   

class UpVote(models.Model):
    """Model UpVote extends django.db.models.Model inbuilt class for storing Upvoted reply instance with user who Upvoted.
    :param model.Model: django.db.models.Model class act as a superclass for the Upvote model.
    :type models.Model: class
    """
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='upvote_user')

class DownVote(models.Model):

    """Model DownVote extends django.db.models.Model inbuilt class for storing Downvoted reply instance with user who Downvoted.
    :param model.Model: django.db.models.Model class act as a superclass for the Downvote model.
    :type models.Model: class
    """
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='downvote_user')

class Like(models.Model):
    """Model Like extends django.db.models.Model inbuilt class and create a database table for storing liked question instance with corresponding user.
    :param model.Model: django.db.models.Model class act as a superclass for the new model class.
    :type models.Model: class
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='like_user')

class Dislike(models.Model):
    """Model Dislike extends django.db.models.Model inbuilt class and create a databse table for storing disliked question instance with corresponding user.
    :param model.Model: django.db.models.Model class act as a superclass for the new model class.
    :type models.Model: class
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='dislike_user')

class Notify(models.Model):
    message = models.CharField(max_length=1000)
    user_name = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
   
