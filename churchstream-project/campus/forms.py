from django.forms import ModelForm
from campus.models import StreamEvent, Video
from campus.models import Video
from django import forms

class StreamEventForm(ModelForm):
    class Meta:
        model = StreamEvent
        fields = ['title','welcome_message','question','response1','response2','response3','devotional','prayer']

class VideoForm(forms.ModelForm):
    class Meta: #this, it seems, is necessary if you are getting your form data from a model
        model = Video
        fields = ['url']
        labels = {'url':'YouTube URL'}

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for YouTube videos:')
