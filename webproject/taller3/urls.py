from django.urls import path
from django.views.generic import TemplateView
from taller3 import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    path('taller3', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    ]