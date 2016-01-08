from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from bakery.views import BuildableListView, BuildableDetailView
from datetime import date

from .models import Camera, Photo, TimeLapse

class CameraListView(BuildableListView):
    model = Camera
    template_name = 'index.html'
    
class CameraDetailView(BuildableDetailView):
    model = Camera
    template_name = 'camera.html'
    slug_field = 'camera_slug'
    def get_object(self):
        return Camera.objects.get(camera_slug=self.kwargs.get("camera_slug"))
    def get_context_data(self, **kwargs):
        #today_year = date.today().year
        #today_month = date.today().month
        #today_day = date.today().day
        today_year = 2015
        today_month = 8
        today_day = 17
        context = super(CameraDetailView, self).get_context_data(**kwargs)
        context['background_photo'] = Photo.objects.filter(camera=self.object, photo_datetime__year=today_year, photo_datetime__month=today_month, photo_datetime__day=today_day).order_by('photo_datetime')[5]
        context['todays_images'] = Photo.objects.filter(camera=self.object, photo_datetime__year=today_year, photo_datetime__month=today_month, photo_datetime__day=today_day).order_by('photo_datetime')
        return context

class CameraDetailTimelapseView(BuildableDetailView):
    model = Camera
    template_name = 'timelapse.html'
    slug_field = 'camera_slug'
    def get_object(self):
        return Camera.objects.get(camera_slug=self.kwargs.get("camera_slug"))
    def get_context_data(self, **kwargs):
        #today_year = date.today().year
        #today_month = date.today().month
        #today_day = date.today().day
        today_year = 2015
        today_month = 8
        today_day = 17
        context = super(CameraDetailTimelapseView, self).get_context_data(**kwargs)
        context['todays_timelapse'] = TimeLapse.objects.get(camera=self.object, movie_date__year=today_year, movie_date__month=today_month, movie_date__day=today_day)
        return context

""""
def camera(request, slug):
	today_year = date.today().year
	today_month = date.today().month
	today_day = date.today().day

	camera = get_object_or_404(Camera, name_slug=slug)
	todays_images = Photo.objects.filter(camera=camera, photo_datetime__year=today_year, photo_datetime__month=today_month, photo_datetime__day=today_day)
	# todays_images = Photo.objects.filter(camera=camera.number)

	# TODO - Create Deep Time Object for querying
	# deep_time_images = OBJECT.objects.filter(camera=camera)
	try:
		yesterday_timelapse = TimeLapse.objects.get(camera=camera, movie_date__year=today_year, movie_date__month=today_month, movie_date__day=today_day-1   +1)
	except ObjectDoesNotExist:
		yesterday_timelapse = None

	context = {
		'camera': camera,
		'todays_images': todays_images,
		'yesterday_timelapse': yesterday_timelapse
		# ,
		# 'deep_time_images': deep_time_images
	}
	return render(request, 'camera.html', context)

def archive(request):
	camera_list = Camera.objects.all()
	context = { 'camera_list': camera_list, }
	return render(request, 'archive.html', context)

def archive_camera(request, slug):
	camera = Camera.objects.get(name_slug=slug) # Get camera object based off of slug in URL
	context = { 'camera': camera, }
	return render(request, 'archive_camera.html', context)

def archive_camera_day(request, slug, year, month, day):
	camera = Camera.objects.get(name_slug=slug) # Get camera object based off of slug in URL
	photo_list = Photo.objects.filter(camera=camera.number, photo_datetime__year=year, photo_datetime__month=month, photo_datetime__day=day,)
	context = {
		'photo_list': photo_list,
		'camera': camera,
		'year': year,
		'month': month,
		'day': day,
	}
	return render(request, 'archive_camera_day.html', context)
    
"""