import os
import requests
from urllib import request
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


def github_callback(request):

    # github 로그인을 요청하면
    # github_login 메서드에서 보듯이 github은 사용자를 다시 이 웹사이트로 redirect한다.(github/callback)
    # 이후 이 웹사이트(app)은 access token을 이용해 api에 접근함
    # request객체 내에 있는 code값으로 이 token과 맞바꿔올수있음

    print(request.GET)
    print(request.GET.get("code"))

    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code", None)

    print(client_id + " " + client_secret + " " + code)

    if code is not None:
        result = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        # 코드를 token과 바꾸기 위해 위 url에 post request를 보냄
        # token은 response객체에 들어있거나 json으로 받을 수 있음
        result_json = result.json()
        error = result_json.get("error", None)
        if error is not None:
            return redirect(reverse("users:login"))
        else:
            # json으로 받아온 token으로 깃헙 로그인 api에 접근
            access_token = result_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            # api에 접근이 성공한다면, 회원에 대한 여러 정보를 json으로 받아볼수있다.
            profile_json = profile_request.json()
            username = profile_json.get("login", None)
            if username is not None:
                name = profile_json.get("name")
                email = profile_json.get("email")
                bio = profile_json.get("bio")
                user = models.User.objects.get(email=email)
                # 이 이메일을 가진 유저가 있다면 그건 이미 로그인이 돼있다는 뜻일것.
                if user is not None:
                    return redirect(reverse("users:login"))
                else:
                    user = models.User.objects.create(
                        username=email, first_name=name, bio=bio, email=email
                    )
                    login(request, user)
                    return redirect(reverse("core:home"))
            else:
                return redirect(reverse("users:login"))
    else:
        return redirect(reverse("core:home"))
