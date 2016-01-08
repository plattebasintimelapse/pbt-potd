from django.contrib import admin

from timelapse.models import Camera, Photo, TimeLapse

class CameraAdmin(admin.ModelAdmin):
    prepopulated_fields = {"camera_slug": ("name",)}

admin.site.register(Camera, CameraAdmin)
admin.site.register(Photo)
admin.site.register(TimeLapse)