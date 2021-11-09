from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()  # 아이템들이 쓰이는 방의 개수?


class PhotoInLine(admin.TabularInline):

    model = models.Photo


# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInLine,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Spaces", {"fields": ("guests", "bedrooms", "beds", "baths")}),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About The Space",
            {
                "classes": ("collapse",),
                "fields": ("facilities", "amenities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        # "description",
        "name",
        "country",
        "city",
        "price",
        "address",
        "host",
        "guests",
        "bedrooms",
        "beds",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        # "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)
    # fields = ("country",)
    search_fields = ("^city", "^host__username")
    # search_fields = ("^city", "host")  # foreign key면 prefix 안먹힘?
    filter_horizontal = (
        "facilities",
        "amenities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.all().count()

    def count_photos(self, obj):
        return obj.photos.count()

    # count_amenities.short_description = "hello sexy"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # print(obj.file.url)
        # print(type(obj.file))
        # return obj.file.url
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
