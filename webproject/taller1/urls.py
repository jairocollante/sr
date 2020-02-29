from django.urls import path
from django.views.generic import TemplateView
from taller1 import views
from taller1.views import T1LoginView, T1PerfilView, T1Userid_ProfileList,T1Userid_ProfileFormView, T1Userid_TimestampFormView,T1ModeloUserUser,T1ModeloItemItem


urlpatterns = [

    path('', TemplateView.as_view(template_name='taller1/index.html'), name='t1_index'),
    path('login', T1LoginView.as_view(), name='t1_login'),
    path('perfil', T1PerfilView.as_view(), name='t1_perfil'),
    path('usuarios', T1Userid_ProfileList.as_view(), name='t1_listaUsuarios'),
    path('nuevoPerfil', T1Userid_ProfileFormView.as_view(), name='t1_nuevoP'),  
	path('nuevoTimestamp', T1Userid_TimestampFormView.as_view(), name='t1_nuevoT'), 
    path('modeloUU', T1ModeloUserUser.as_view(), name='t1_modeloUU'),
    path('modeloII', T1ModeloItemItem.as_view(), name='t1_modeloII'),	
	
    
    ] 