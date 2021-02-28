from django.contrib import admin
from django.urls import path, include
from campus import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('<str:campusid>/', views.CampusPage, name='campus_page'),
    path('<str:campusid>/create/', views.CreateStreamEvent,name='create_streamevent'),
    # path('<str:campusid>/create/', views.CreateStreamEvent.as_view(),name='create_streamevent'),
    path('<str:campusid>/<int:pk>/', views.DetailStreamEvent.as_view(),name='detail_streamevent'),
    path('<str:campusid>/<int:pk>/update/', views.UpdateStreamEvent.as_view(),name='update_streamevent'),
    path('<str:campusid>/<int:pk>/addvideo', views.add_video,name='add_video'),
    path('<str:campusid>/<int:sepk>/<int:pk>/deletevideo', views.DeleteVideo.as_view(),name='delete_video'),

]
