from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 해당 필드값을 확인하고 싶은 경우 반드시 "clean_"이어야 함.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")
