from django.shortcuts import render
from django.views import View
from . import forms


class LoginView(View):

    # GET 방식
    def get(self, request):
        # form = forms.LoginForm()
        form = forms.LoginForm(initial={"email": "asdf@asdf.com"})
        # print("GET - form.as_p [%s]" % form.as_p)
        return render(request, "users/login.html", {"form": form})

    # POST 방식
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        print("POST - is_valid() [%s]" % form.is_valid())
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
