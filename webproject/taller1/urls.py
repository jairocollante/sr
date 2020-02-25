from django.urls import path
from taller1 import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('ex1', views.ex1, name='ex1'),
    
    ] 