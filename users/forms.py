from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholeder": "Password"})
    )

    # 해당 필드값을 확인하고 싶은 경우 반드시 "clean_"이어야 함.

    # 서로 종속돼있는(depends)필드들을 검증할 경우 : 각각의 필드에 대해 cleaned_data를 갖는 clean 메서드
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(None, forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):

    ## Model Form은 field의 uniqueness를 알아서 검증해준다
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        password_validation.validate_password(password1, self.instance)

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match!")
        else:
            return password

    def save(self, commit: bool = ...):
        user = super().save(commit=False)
        # 위의 정보로 user객체를 생성하긴 하는데 db에 commit은 안함

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)

        print(user.username)
        user.save()
        # 새로 원하는 필드값을 만든 뒤에 user객체에 덮어씌우기 후 save & commit
