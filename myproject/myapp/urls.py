# myapp/urls.py
#-------------------------------------------------------------
# For this file we'll use the index html in template folde

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
