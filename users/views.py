from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):

    # GET 방식
    def get(self, request):
        # form = forms.LoginForm()
        form = forms.LoginForm(initial={"email": "awbwd4@gmail.com"})
        # print("GET - form.as_p [%s]" % form.as_p)
        return render(request, "users/login.html", {"form": form})

    # POST 방식
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print("cleand_data [%s]" % form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})
        print(form)


# cleand_data는 모든 필드를 정리해준 것에 대한 결과이다.
# 만약 clean_method를 선언했는데
# 이 메서드가 아무것도 return하지 않는다면
# 해당 필드를 지워버린다.
# 즉 clean_email메서드의 return값이 없다면,
# email 필드는 null 값을 갖느다.


def login_view(request):
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
