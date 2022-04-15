import os
import requests
from urllib import request
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
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
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    # form_class = UserCreationForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     "first_name": "Jaeuk",
    #     "last_name": "Ko",
    #     "email": "endlesswaltz0@naver.com",
    # }
    print("=============1==================")

    def form_valid(self, form):
        form.save()

        # 가입이 성공하면 바로 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        print("===========2==================== ")
        if user is not None:
            login(self.request, user)

        # 계정 생성이 완료된 뒤에 이메일을 발송함
        print("============3=================== ")
        user.verify_email()
        print("=============4================== ")

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


## 깃헙 로그인


class GithubException(Exception):
    pass


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
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # 코드를 token과 바꾸기 위해 위 url에 post request를 보냄
            # token은 response객체에 들어있거나 json으로 받을 수 있음
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                # json으로 받아온 token으로 깃헙 로그인 api에 접근
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                print("profile_request.json() : [%s]" % profile_request.json())
                # api에 접근이 성공한다면, 회원에 대한 여러 정보를 json으로 받아볼수있다.
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                # "login"에 값이 정상적으로 박히면, api가 정상 실행됐다는 것.
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    profile_image = profile_json.get("avatar_url")

                    # 해당 이메일을 가진 다른 유저는 없는가?
                    try:
                        # 이미 이 웹사이트에 가입돼있는 github 회원인 경우 : 유저가 가입이 아닌 로그인을 원한다는것.
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            # github 로그인으로 들어왔지만 password나 kakao로 가입된 회원일 상황
                            print(
                                "========user login method is not github  [%s]========="
                                % models.User.login_method
                            )
                            raise GithubException(
                                f"Please log in with : {user.login_method}"
                            )
                        else:
                            print(
                                "======== user already exists, log user in now ========="
                            )
                    except models.User.DoesNotExist:
                        print(
                            "======== user does not exists, create user now ========="
                        )
                        # github의 계정이 이 웹사이트에 없는 회원일 경우
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{name}-avatar", ContentFile(photo_request.content)
                            )
                    # 기존회원이든 신규 생성한 회원이든 로그인을 한 뒤에 home으로 보낸다.
                    login(request, user)
                    messages.success(request, f"Welcome back! {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    # api가 정상 실행되지 않았음.
                    print("========username is None==========")
                    raise GithubException("Can't get your profile!")
        else:
            raise GithubException("Can't get code!")
    except GithubException as e:
        # send error message
        messages.error(request, e)
        return redirect(reverse("users:login"))


### 카카오 로그인
class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    print("kakao api key [%s]" % client_id)
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=account_email"
    )


def kakao_callback(request):
    # git과 같이, 인증 api에 접근하기 위한 토근 발행. code는 리다이렉트 하면서 카카오 서버에서 줬음.
    try:
        code = request.GET.get("code")
        # raise KakaoException("Something went wrong!!")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"code={code}"
        )
        token_json = token_request.json()

        error = token_json.get("error", None)
        # token을 받아올때 에러가 나는지 안나는지. 에러가 난다면 json내부에는 "access code"가 아니라 "error" 필드가 생긴다.
        if error is not None:
            raise KakaoException("Can't get Authorization Code")

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print("========profile_request.json() [%s]" % profile_request.json())

        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        email = profile_json.get("kakao_account").get("email")
        nickname = email.split("@")[0]

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with : {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
        messages.success(request, f"Welcome back! {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    pass
