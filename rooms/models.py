from django.db import models
from django.urls import reverse
from django.db.models.deletion import PROTECT
from core import models as core_models
from django_countries.fields import CountryField


# from django_cities.fields import CountryField
# from cities.models

# from users import models as user_models


# from django_countries

# Create your models here.


class AbstractItem(core_models.TimeStampModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)
    # name2 = models.CharField(max_length=80)
    # 왜 name2를 추가하니 에러가 날까?

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Object Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facilities Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    file = models.ImageField(upload_to="room_photos")
    # photo를 room과 연결시킴
    # String 으로 하면 django가 자동으로 room 클래스를 읽는다.


class Room(core_models.TimeStampModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    # city
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        print(self.city)
        super().save(*args, **kwargs)

    # 원하는 model을 찾을 수 있는 url을 리턴함.
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        # all_ratings = []
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()

        if len(all_reviews) > 0:
            return round(all_ratings / len(all_reviews), 2)
            # return all_ratings / all_reviews
        else:
            return 0
