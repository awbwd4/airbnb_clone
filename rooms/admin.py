from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

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
        # "facilities",
        "count_amenities",
        # "house_rules",
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

    # count_amenities.short_description = "hello sexy"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    pass
