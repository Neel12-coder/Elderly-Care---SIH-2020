"""ElderlyCare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path

from .views import displayPage,testingPage,testing,locationPage,storeCurrentLocation,predictFromDoctor,predictForDoctor
from .views import landingPage,dashboardPage

urlpatterns = [

     path('base', displayPage, name='displayPage'),
     path('', landingPage, name='landingPage'),
     path('patient_dash',dashboardPage,name='dashboardPage'),
     path('location', locationPage, name='locationPage'),
     path('location/<str:lat>/<str:long>', storeCurrentLocation, name='storeCurrentLocation'),
     path('base3', testingPage, name='testingPage'),
     path('relative_dash', testing, name='testing'),
     path('doctorcheckprobability',predictForDoctor,name='predictFromDoctor'), 
     path('doctorshowprobability',predictFromDoctor,name='predictforDoctor')

]

