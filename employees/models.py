import re
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator   
from django.core.validators import RegexValidator
# from django.core.validators import validate_email
# from django.forms import ValidationError


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


