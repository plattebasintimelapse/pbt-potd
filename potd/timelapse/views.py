from django.shortcuts import get_object_or_404, render
from datetime import date

from .models import Camera, Photo

def index(request):
    camera_list = Camera.objects.all()
    context = { 'camera_list': camera_list, }
    return render(request, 'index.html', context)

def camera(request, slug):
	camera = get_object_or_404(Camera, name_slug=slug)
	# todays_images = Photo.objects.filter(camera=camera.number, photo_datetime__year=date.today().year, photo_datetime__month=date.today().month, photo_datetime__day=date.today().day)
	todays_images = Photo.objects.filter(camera=camera.number)
	context = {
		'camera': camera,
		'todays_images': todays_images
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
	cam_num = camera.number 					# Assign camera number to be used in Photo query
	photo_list = Photo.objects.filter(camera=cam_num, photo_datetime__year=year, photo_datetime__month=month, photo_datetime__day=day,)
	context = {
		'photo_list': photo_list,
		'camera': camera,
		'year': year,
		'month': month,
		'day': day,
	}
	return render(request, 'archive_camera_day.html', context)