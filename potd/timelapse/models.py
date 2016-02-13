from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=255)
    camera_slug = models.SlugField()
    number = models.CharField(max_length=4, blank=True, null=True)
    location_x = models.FloatField()
    location_y = models.FloatField()
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    iconic_photo = models.ImageField(upload_to='iconicphotos/', blank=True, null=True)
    def get_absolute_url(self):
        return "/%s/" % self.camera_slug
    def get_timelapse_url(self):
        return "/%s/timelapse/" % self.camera_slug
    def __str__(self):
        return self.name
        
class Photo(models.Model):
    camera = models.ForeignKey(Camera)
    photo = models.ImageField(upload_to='photos/')
    photo_description = models.TextField(blank=True, null=True)
    photo_datetime = models.DateTimeField()
    photo_aperture = models.CharField(max_length=50, blank=True, null=True)
    photo_shutter_speed = models.CharField(max_length=50, blank=True, null=True)
    photo_iso = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return "%s from %s" % (self.id, self.camera.name)
        
class TimeLapse(models.Model):
    camera = models.ForeignKey(Camera)
    movie = models.FileField(upload_to='movies/')
    movie_date = models.DateTimeField()
    movie_description = models.TextField(blank=True, null=True)
    def __str__(self):
        return "%s from %s" % (self.movie_date, self.camera.name)
    def get_absolute_url(self):
        return "/%s/timelapse/" % self.camera.camera_slug
