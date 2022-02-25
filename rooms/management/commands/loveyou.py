from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates amenities"

    # print("hello")

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            help="how many times do you want me to tell you that I love you",
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            # print("i love you")
            self.stdout.write(self.style.ERROR("I love you"))
