import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="how many rooms do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        # -- 운영에서는 절대 all objects를 가져오지 말것 특히 db가 클 경우!
        room_types = room_models.RoomType.objects.all()
        # price = room_models.Room.price
        print(room_types, all_user)
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "guests": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )

        created_photos = seeder.execute()
        # created_clean = flatten(
        #     list(("created_photos.values() : ", created_photos.values()))
        # )

        created_clean = flatten(list(created_photos.values()))

        print(created_clean)

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(1, random.randint(10, 17)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    # file=f"room_photos/{random.randint(1,2)}.webp",
                    file=f"uploads/room_photos/2.webp",
                )

        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created!!"))
