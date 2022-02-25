from django.core.management.base import BaseCommand

# from rooms import models as room_models
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates amenities"

    # print("hello")

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times",
    #         help="how many times do you want me to tell you that I love you",
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workspace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Shampoo",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)  ## a라는 Amenity 객체 생성
        self.stdout.write(self.style.SUCCESS("Amenities Created!!"))

        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.SUCCESS("i love you"))
