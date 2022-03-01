# from django.http import Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries
from . import models


##ListView를 사용한 ClassBasedView
class HomeView(ListView):

    ###제네릭view인 ListView는 템플릿명이 명시적으로 지정되지 않을 경우
    ### 디폴트로 "모델명_list.html"을 템플릿 명으로 사용한다.
    ###이 경우에는 models.Room을 사용하므로 "room_list.html"

    """Home View Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context[""] =
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now

        return context


class RoomDetail(DetailView):

    ###제네릭view인 DetailView 템플릿명이 명시적으로 지정되지 않을 경우
    ### 디폴트로 "모델명_detial.html"을 템플릿 명으로 사용한다.
    ###이 경우에는 models.Room을 사용하므로 "room_detail.html"

    """RoomDetail Definition"""

    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    print(city)
    city = str.capitalize(city)  ##db가 대문자로 시작함
    return render(
        request,
        "rooms/search.html",
        {"city": city, "countries": countries},
    )


# 방 디테일 뷰의 fbv
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         print(pk)
#         print(room)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect("/")
#         # return redirect(reverse("core:home"))
#         raise Http404()


# from math import ceil
# from datetime import datetime
# from pickle import TRUE
# from django.core.paginator import Paginator, EmptyPage

# django의 paginator 사용
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")


# django의 paginator를 사용하지 않고 순수 파이썬 만으로 페이징 기능 구현
# def all_rooms(request):
#     print(request.GET.get("page", 1))
#     page = request.GET.get("page", 1)
#     page = int(page or 1)
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     ## page : 2 -> 10~20까지 보여줘야 함 -> limit = 10*2 = 20 // offset = 20-10 = 10
#     all_rooms = models.Room.objects.all()[offset:limit]
#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count),
#         },
#     )
