import re
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator   
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

def validate_ephone(value):
    pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number.')

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    ename = models.CharField('ename',max_length=100)
    ephone = models.CharField('ephone', max_length=15,validators = [validate_ephone])
    eemail = models.CharField('eemail', max_length=100 )
    edepartment = models.CharField('edepartment',max_length=20)


    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    contactno = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username