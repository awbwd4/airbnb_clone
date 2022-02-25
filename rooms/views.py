from math import ceil
from datetime import datetime
from pickle import TRUE
from django.shortcuts import render
from . import models


def all_rooms(request):
    print(request.GET.get("page", 1))
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    ## page : 2 -> 10~20까지 보여줘야 함 -> limit = 10*2 = 20 // offset = 20-10 = 10
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
