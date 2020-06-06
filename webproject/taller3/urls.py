from django.urls import path
from django.views.generic import TemplateView
from taller3 import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    path('taller3', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    path('login', views.T3LoginView.as_view(), name='t3_login'),
    path('sistema/', views.T3RecommenderView.as_view(), name='t3_sistema'),
    path('movies/', views.T3MoviesView.as_view(), name='t3_movies'),
    path('newUser', views.T3UserFormView.as_view(), name='t3_newUser'),  
    path('search', views.T3SearchFormView.as_view(), name='t3_search'),  
    path('found', views.T3FoundFormView.as_view(), name='t3_found'),  
    ]