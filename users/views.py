from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


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
        print("cleand_data [%s]" % form.cleaned_data)
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
        "email": "jaeuk@naver.com",
    }

    def form_valid(self, form):
        form.save()

        # 가입이 성공하면 바로 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)
