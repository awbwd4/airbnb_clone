import os
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # success_url = reverse("core:home")
    # reverse : "core:home"으로 되돌려 보내주도록 되어 있으나
    # 이 클래스(form)을 가져올때는 url은 아직 호출이 되지 않은 상태임.
    # 즉, config.url이 아직 어떤 패턴도 갖고 있지 않음.
    # reverse_lazy : reverse랑 같은 기능이긴 한데, 자동으로 url을 호출하진 않음.
    # view가 필요할때만 호출

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# cleand_data는 모든 필드를 정리해준 것에 대한 결과이다.
# 만약 clean_method를 선언했는데
# 이 메서드가 아무것도 return하지 않는다면
# 해당 필드를 지워버린다.
# 즉 clean_email메서드의 return값이 없다면,
# email 필드는 null 값을 갖느다.


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Jaeuk",
        "last_name": "Ko",
        "email": "endlesswaltz0@naver.com",
    }

    def form_valid(self, form):
        form.save()

        # 가입이 성공하면 바로 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        # 계정 생성이 완료된 뒤에 이메일을 발송함
        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, key):
    print(request)
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        print("complete_verification_key [%s]" % key)
        # to do : add success msg
    except models.User.DoesNotExist:
        # to do : add error msg
        pass
    return redirect(reverse("core:home"))


def github_login(request):

    # O auth 작동 원리!
    # 여기서 view는 아무것도 render하지 않는다
    # 대신,  github로 redirect해줄것
    # 그 후 사용자가 github에 로그인 하고 git에서 이 웹 애플리케이션을 accept하게 되면,
    # github는 사용자를 다시 이 웹 애플리케이션(우리 웹사이트)로 redirect한다.
    # 따라서 "authorization call back URL"은 github가 이 웹사이트를 accept한 뒤 사용자를 돌려보낼 url이다.

    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(reqeust):
    pass
