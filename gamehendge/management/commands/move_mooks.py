from django.core.management.base import BaseCommand, CommandError
from gamehendge import logic

class Command(BaseCommand):

    def handle(self, *args, **options):
        logic.move_mooks()
