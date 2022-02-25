import faker
import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="how many reviews do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "reviews": lambda x: seeder.faker.sentence(),
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(1, 10),
                "cleanliness": lambda x: random.randint(1, 10),
                "location": lambda x: random.randint(1, 10),
                "check_in": lambda x: random.randint(1, 10),
                "value": lambda x: random.randint(1, 10),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )

        created_reviews = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!!"))
