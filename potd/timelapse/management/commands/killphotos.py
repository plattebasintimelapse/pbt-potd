from django.core.management.base import BaseCommand, CommandError
from timelapse.models import Photo
from datetime import date

class Command(BaseCommand):
    help = 'Deletes all photos from that day'

    def handle(self, *args, **options):
        p = Photo.objects.filter(photo_datetime__day=date.today().day, photo_datetime__month=date.today().month, photo_datetime__year=date.today().year)
        p.delete()

