from django.contrib import admin
from django.urls import path,include,re_path
from API.views import default

urlpatterns = [
    path('api/',include('API.urls')),

    re_path(r'^(?!api).+|',default,name='default'),
]   
