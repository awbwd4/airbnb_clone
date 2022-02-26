from django.utils import timezone
from django.views.generic import ListView
from . import models


##ListView를 사용한 ClassBasedView
class HomeView(ListView):

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


# from math import ceil
# from datetime import datetime
# from pickle import TRUE
# from django.shortcuts import render, redirect
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
