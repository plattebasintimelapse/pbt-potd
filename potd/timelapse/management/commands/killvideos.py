from django.core.management.base import BaseCommand, CommandError
from timelapse.models import TimeLapse
from datetime import date
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes all TimeLapse videos from that two days ago'

    def handle(self, *args, **options): 
        t = TimeLapse.objects.filter(movie_date=(date.today()-timedelta(2)))
        t.delete()


