from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 10,unique=True)
    fname = models.CharField(max_length = 20,default='')
    lname = models.CharField(max_length = 20,default='')
    email = models.EmailField(unique=True,default='')
    timestamp = models.DateTimeField(auto_now_add=True , blank=True)
    def __str__(self):
        return 'Registered user ' + self.username


class Tweet(models.Model):
    tweet_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length = 140)
    timestamp = models.DateTimeField(auto_now_add=True , blank=True)
   
    def __str__(self):
        return 'Tweet by '+self.user_id + ': ' + self.tweet_id