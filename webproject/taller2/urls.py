from django.urls import path
from django.views.generic import TemplateView
from taller2 import views
from taller2.views import T2LoginView

urlpatterns = [
    path('', TemplateView.as_view(template_name='taller2/index.html'), name='t2_index'),
    path('taller2', TemplateView.as_view(template_name='taller2/index.html'), name='t2_index'),
    path('login', T2LoginView.as_view(), name='t2_login'),
    ]