import re
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator   
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

def validate_ephone(value):
    pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
    validator = RegexValidator(pattern, 'Invalid phone number.')
    validator(value)


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    ename = models.CharField('ename',max_length=100)
    ephone = models.CharField('ephone', max_length=15,validators = [validate_ephone])
    eemail = models.CharField('eemail', max_length=100 )
    edepartment = models.CharField('edepartment',max_length=20)


    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # Add any additional fields you want for your user model
    # For example, you might want to include fields for name, date of birth, etc.
    # email is already included in AbstractUser
    def __str__(self):
        return self.username

    class Meta:
        pass
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
