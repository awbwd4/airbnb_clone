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

    ### 깃 테스트햣

    """RoomDetail Definition"""

    model = models.Room


def search(request):

    """url에서 값을 가져오는 부분"""
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)  ##db가 대문자로 시작함
    # 검색바가 아닌 url에 아무런 조건이 없을경우 "Anywhere"
    if len(city) == 0:
        city = "Anywhere"
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    print(s_amenities, s_facilities)

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_faicilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    """model에 저장돼있는 값을 가져오는 부분"""
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "room_types": room_types,
        "countries": countries,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},  # 두개의 dic 타입을 합치는 방법
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
