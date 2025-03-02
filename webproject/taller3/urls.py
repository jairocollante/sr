from django.urls import path
from django.views.generic import TemplateView
from taller3 import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    path('taller3', TemplateView.as_view(template_name='taller3/index.html'), name='t3_index'),
    path('login', views.T3LoginView.as_view(), name='t3_login'),
    path('sistema/', views.T3RecommenderView.as_view(), name='t3_sistema'),
    path('sistema2/', views.T3RecommenderView2.as_view(), name='t3_sistema2'),
    path('movies/', views.T3MoviesView.as_view(), name='t3_movies'),
    path('newUser', views.T3UserFormView.as_view(), name='t3_newUser'),  
    path('search', views.T3SearchFormView.as_view(), name='t3_search'),  
    path('found', TemplateView.as_view(), name='t3_found'),  
    path('rating', views.T3RatingSave, name='t3_rating'),  
    ]