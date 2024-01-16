from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class EmpForm(forms.Form):
    eid = forms.IntegerField()
    ename = forms.CharField(required=True, min_length=1, max_length=50)
    ephone = forms.CharField(required=True,validators=[RegexValidator(r'^(?:\+91|0)?[6-9]\d{9}$', 'Invalid phone number.')])
    email = forms.CharField(required=True)
    department = forms.CharField(required=True, min_length=1, max_length=100)

