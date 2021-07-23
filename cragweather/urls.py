from django.urls import path

from . import views

urlpatterns = [
  path('', views.addToDatabase, name='addToDataBase'),
  path('', views.buildLocationInDatabase, name='buildLocationInDatabase')
]
