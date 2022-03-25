# from django.http import Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django_countries import countries
from math import ceil
from . import models, forms


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


class SearchView(ListView):

    """SearchView Definition"""

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)
            # form에 request객체를 연결하면 bounded form이 된다
            # 자동으로 데이터 정합성을 체크하게됨.
            if form.is_valid():  # form의 이상여부 체크
                print(form.cleaned_data)

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                ## 검색조건 필터링
                filter_args = {}

                ### 검색조건 1 : 도시
                ## 검색조건 생성
                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                ### 검색조건 2 : 국가
                filter_args["country"] = country
                ### 검색조건 3 : 방 종류
                if room_type is not None:
                    filter_args["room_type"] = room_type  # room_type의 pk와 정확히 일치해야 함.
                ### 검색조건 4 : 가격
                if price is not None:
                    filter_args["price__lte"] = price  # 고객이 지불하려는 최대 가격
                ### 검색조건 5 : 게스트 수
                if guests is not None:
                    filter_args["guests__gte"] = guests  # 게스트 수와 같거나 더 많은 수를 수용할 수 있는 방
                ### 검색조건 6 : 침실 수
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                ### 검색조건 7 : 침대 수
                if beds is not None:
                    filter_args["beds__gte"] = beds
                ### 검색조건 8 : 화장실 수
                if baths is not None:
                    filter_args["baths__gte"] = baths
                ### 검색조건 9 : 즉시 예약 가능 여부
                if bool(instant_book) is True:
                    filter_args["instant_book"] = True
                ### 검색조건 10 : 즉시 예약 가능 여부
                if bool(superhost) is True:
                    filter_args["host__superhost"] = True
                    # room 모델에는 superhost여부를 따로 갖고있지 않고
                    # user를 fk로 갖고만 있다.
                    # user모델 안에 들어가면 해당 객체는 superhost여부를 필드값으로 갖고있음.

                ## 검색조건 출력
                print(filter_args)

                rooms = models.Room.objects.filter(**filter_args)

                rooms = rooms.order_by("created")

                ### 검색조건 11 : amenity
                for amenity in amenities:
                    # filter_args["amenities__pk"] = int(s_amenity)
                    rooms = rooms.filter(amenities=amenity)
                ### 검색조건 12 : facility
                for facility in facilities:
                    # filter_args["facilities__pk"] = int(s_facility)
                    rooms = rooms.filter(facilities=facility)

                print(dir(rooms))
                print(rooms.count())

                all_rooms_count = rooms.count()

                # 페이지네이팅
                # page = request.GET.get("page", 1)
                # paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)

                print(page)
                page = int(page or 1)
                page_size = 10
                limit = page_size * page
                offset = limit - page_size
                ## page : 2 -> 10~20까지 보여줘야 함 -> limit = 10*2 = 20 // offset = 20-10 = 10
                rooms = rooms[offset:limit]
                page_count = ceil(all_rooms_count / page_size)

                try:
                    # rooms = paginator.get_page(page)
                    print(rooms)
                    print(page)
                    print(page_count)
                    return render(
                        request,
                        "rooms/search.html",
                        {
                            "form": form,
                            "rooms": rooms,
                            "page": page,
                            "page_count": page_count,
                            "page_range": range(1, page_count),
                        },
                    )
                except EmptyPage:
                    return redirect("search/")

                # rooms = gs

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
        else:

            page = request.GET.get("page", 1)
            form = forms.SearchForm()
            return render(
                request,
                "rooms/search.html",
                {"form": form, "page": page},
            )
        # url에 "country"의 값이 없다면 unbounded form으로 한다.


# def search(request):


# 방 디테일 뷰의 fbv
# def room_det                  ail(request, pk):
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
