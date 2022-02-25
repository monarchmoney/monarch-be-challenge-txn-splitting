from django.core.management.base import BaseCommand

from monarch.db.models import User
from monarch.development.seed import seed_data_for_user


class Command(BaseCommand):
    help = "Seed transaction data"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email address of user")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        user = User.objects.get(email=email)
        seed_data_for_user(user, reset=True)
