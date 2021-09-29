from django.db import models
from django.db.models.deletion import PROTECT
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models


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

    pass


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    pass


class Facility(AbstractItem):

    """Facilities Model Definition"""

    pass


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    pass


class Room(core_models.TimeStampModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    def __str__(self):
        return self.name
