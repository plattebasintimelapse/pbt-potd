import csv, string, datetime
from django.template import defaultfilters

from django.core.management.base import BaseCommand, CommandError
from timelapse.models import Camera

class Command(BaseCommand):
    help = 'Loads all camera locations into the Camera model'

    def handle(self, *args, **options):
        reader = csv.reader(open("camerametadata.csv", "rU"), dialect=csv.excel)
        reader.next()
        for row in reader:
            cname = row[1]
            cslug = defaultfilters.slugify(cname)
            if len(row[4]) == 1:
                cnum = "00"+row[4]
            elif len(row[4]) == 2:
                cnum = "0"+row[4]
            else:
                cnum = row[4]
            cdesc = row[0]
            cx = row[2]
            cy = row[3]
            c = Camera.objects.get_or_create(name=cname, name_slug=cslug, number=cnum, location_x=cx, location_y=cy, description=cdesc)
            self.stdout.write("Successfully created %s" % cname)