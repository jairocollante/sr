from django.urls import path
from django.views.generic import TemplateView
from taller1 import views
from taller1.views import T1LoginView, T1PerfilView, Userid_ProfileList


urlpatterns = [

    path('', TemplateView.as_view(template_name='taller1/index.html'), name='t1_index'),
    path('login', T1LoginView.as_view(), name='t1_login'),
    path('perfil/<usuario>', T1PerfilView.as_view(), name='t1_perfil'),
    path('usuarios', Userid_ProfileList.as_view(), name='t1_listaUsuarios'),    
    
    ] 