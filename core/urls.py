from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home"),
    # ****path는 url과 함수만을 갖는다!!!!!
    # path(url, 함수, 이름) 이어야함.
    # path("", room_views.all_rooms(), name="home"),
]
