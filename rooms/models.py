from django.db import models
from core import models as core_models
from django_countries.fields import CountryField
from users import models as user_models


# from django_countries

# Create your models here.


class AbstractItem(core_models.TimeStampModel):
    class Meta:
        abstract = True

    """ Abstract Item """
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
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
    room_type = models.ManyToManyField(RoomType, blank=True)

    def __str__(self):
        return self.name
