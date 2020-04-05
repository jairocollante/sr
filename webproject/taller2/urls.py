from django.urls import path
from django.views.generic import TemplateView
from taller2 import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='taller2/index.html'), name='t2_index'),
    ]