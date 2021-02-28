from django.db import models
from django.contrib.auth.models import User

class CampusModel(models.Model):
    campus_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True,default='')
    banner = models.ImageField(upload_to="campus", height_field=None, width_field=None, max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.campus_name

class StreamEvent(models.Model):
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    date_published = models.DateField(auto_now=True, auto_now_add=False)
    campus = models.ForeignKey(CampusModel, on_delete=models.CASCADE)
    #welcome message
    welcome_message = models.TextField(blank=True)
    #questionare
    question = models.CharField(max_length=255, blank=True)
    response1 = models.CharField(max_length=255, blank=True)
    response2 = models.CharField(max_length=255, blank=True)
    response3 = models.CharField(max_length=255, blank=True)
    #devotional
    devotional = models.TextField(blank=True)
    #prayer
    prayer = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    streamevent = models.ForeignKey(StreamEvent, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title
