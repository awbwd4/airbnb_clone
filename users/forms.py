from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(UserCreationForm):

    username = forms.EmailField(label="Email")

    class Meta:
        model = models.User
        fields = ("email",)
        # 오버라이딩을 하여 modelForm을 사용했으면, fields도 오버라이딩 해주든지 해야함
