from django.contrib import admin
from campus.models import CampusModel, StreamEvent, Video

# Register your models here.
admin.site.register(CampusModel)
admin.site.register(StreamEvent)
admin.site.register(Video)
