from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from campus.models import CampusModel, StreamEvent, Video
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404
from campus.forms import StreamEventForm
from campus.forms import VideoForm, SearchForm
from django.forms import formset_factory #this library enables us to create form sets
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
import urllib
import requests

#INSTALLATIONS TO DO
#-----------------------------------------------------------------------------------------
#pipenv install requests
#pipenv install django-widget-tweaks
# for deployment on heroku we need to (pipenv install gunicorn psycopg2-binary)
#-----------------------------------------------------------------------------------------

YOUTUBE_API_KEY = 'AIzaSyA363Ba1vNTlQyvMLCIOJhrNBn-rRbQJJs'

def CampusPage(request, campusid):

    campusobj = CampusModel.objects.filter(campus_name=campusid)

    return render(request, 'campus/campus_page.html',{'campusid':campusid,'campusobj':campusobj})

def CreateStreamEvent(request, campusid):

    # campusobj = CampusModel.objects.filter(campus_name=campusid) #because only one campus will be returned with the campus ID, we can use either get or filter here
    campusobj1 = CampusModel.objects.get(campus_name=campusid) #get gives one specific instance
    campusobj2 = CampusModel.objects.filter(campus_name=campusid) #filter gives all the instances

    if not campusobj1.user == request.user: #if the current user is not the assigned user for the current campus
        raise Http404

    if request.method == 'GET':
        return render(request, 'campus/create_streamevent.html',{'form':StreamEventForm})
    else:
        # try: #this try and except is put in for incase we messed up our code somewhere and we have exceede the lengths of one of the fields
            form = StreamEventForm(request.POST)
            newstreamevent = form.save(commit=False)    #what commit=False does is, it creates the new StreamEventForm object, but does not add
                                                        #add it to the database yet
            newstreamevent.campus = campusobj1          #the form that is filled out does not specify a user yet, because we did not link
                                                                    #the user field from the model to our form (in forms.py) we therefore have to assign
                                                                    #a user to the form object we are adding to the database
            newstreamevent.save()                                   #This adds information to the database
            return render(request, 'campus/campus_page.html',{'campusid':campusid,'campusobj':campusobj2})
        # except ValueError:
        #     return render(request, 'campus/create_streamevent.html',{'form':StreamEventForm, 'error':'bad data passed in. Try again.'})


class DetailStreamEvent(DetailView):
    model = StreamEvent
    template_name = 'campus/detail_streamevent.html'

class UpdateStreamEvent(UpdateView):
    model = StreamEvent
    template_name = 'campus/update_streamevent.html'
    fields = ['title','welcome_message','question','response1','response2','response3','devotional','prayer']

    def get_object(self):
        streamevent = super(UpdateStreamEvent, self).get_object()
        if not streamevent.campus.user == self.request.user:
            raise Http404
        return streamevent

    def get_success_url(self):
          campusid=self.kwargs['campusid']
          key=self.kwargs['pk']
          return reverse_lazy('detail_streamevent', kwargs={'campusid': campusid,'pk':key })

def add_video(request, campusid, pk):
    form = VideoForm()
    search_form = SearchForm()
    #Here we need to make sure that the user belonging to this streamevent object
    # is the only one that can add videos to this streamevent
    campus = CampusModel.objects.get(campus_name=campusid)
    streamevent = StreamEvent.objects.get(pk=pk)
    if not campus.user == request.user: #if the current user is not the assigned user for the current campus
        raise Http404
    if request.method == 'POST':
        # Create the form
        form = VideoForm(request.POST) #this initializes the model form with the data in the request
        # now we have to validate the form
        if form.is_valid(): # is_valid() method validates the form to see if all fields have been filled in correctly
            video = Video()
            video.streamevent = streamevent
            video.url = form.cleaned_data['url']

            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v') # this is how we get the youtube ID from the url
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={YOUTUBE_API_KEY}')
                #this request will now go out to the youtube API and get the video we ask for
                json = response.json() #the response we get back is raw data, we need to turn it into a json object
                title = json["items"][0]['snippet']['title']
                #print(title)
                video.title = title
                video.save() #this puts the model in our database
                return redirect('detail_streamevent', campusid, pk)
            else:
                errors = form._errors.setdefault('url', ErrorList()) #the 'url' here refers to the url field in the form
                errors.append('Needs to be a Youtube URL') #here we are adding to the error list that we are calling in the detail_streamevent.html

    return render(request, 'campus/add_video.html', {'form':form, 'search_form':search_form, 'streamevent':streamevent})

def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})

class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'campus/delete_video.html'

    def get_success_url(self):
          campusid=self.kwargs['campusid']
          key=self.kwargs['sepk']
          return reverse_lazy('detail_streamevent', kwargs={'campusid': campusid,'pk':key })

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.streamevent.campus.user == self.request.user:
            raise Http404
        return video
