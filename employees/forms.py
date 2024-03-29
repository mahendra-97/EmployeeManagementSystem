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

class UserForm(forms.Form):
    username = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150)
    contactno = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match"
            )