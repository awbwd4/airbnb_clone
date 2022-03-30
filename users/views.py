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
