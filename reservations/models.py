from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models.deletion import CASCADE
from core import models as core_models


class Reservation(core_models.TimeStampModel):

    """Reservatino Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirmed"
    STATUS_CANCEl = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRM, "Confirmed"),
        (STATUS_CANCEl, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=CASCADE
    )

    def __str__(self):
        return f"{self.room}-{self.check_in}"
        # return self.room.name

    def in_progress(self):
        # now = timezone.now().date()
        # now = timezone.localtime()
        now = parse_date(timezone.localtime().strftime("%Y-%m-%d"))
        print(now)
        print(self.check_in)
        print(self.check_out)
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = parse_date(timezone.localtime().strftime("%Y-%m-%d"))
        return now > self.check_out

    is_finished.boolean = True
