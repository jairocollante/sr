from django.urls import path
from django.views.generic import TemplateView
from taller1 import views
from taller1.views import T1LoginView, T1PerfilView, T1Userid_ProfileList,T1Userid_ProfileFormView, T1Userid_TimestampFormView,T1ModeloUserUserJ,T1ModeloUserUserC,T1ModeloUserUserP,T1ModeloItemItemJ,T1ModeloItemItemC,T1ModeloItemItemP


urlpatterns = [

    path('', TemplateView.as_view(template_name='taller1/index.html'), name='t1_index'),
    path('login', T1LoginView.as_view(), name='t1_login'),
    path('perfil', T1PerfilView.as_view(), name='t1_perfil'),
    path('usuarios', T1Userid_ProfileList.as_view(), name='t1_listaUsuarios'),
    path('nuevoPerfil', T1Userid_ProfileFormView.as_view(), name='t1_nuevoP'),  
    path('nuevoTimestamp', T1Userid_TimestampFormView.as_view(), name='t1_nuevoT'),
    path('modeloUUJ', T1ModeloUserUserJ.as_view(), name='t1_modeloUU_J'),
    path('modeloUUC', T1ModeloUserUserC.as_view(), name='t1_modeloUU_C'),
    path('modeloUUP', T1ModeloUserUserP.as_view(), name='t1_modeloUU_P'),
    path('modeloIIJ', T1ModeloItemItemJ.as_view(), name='t1_modeloII_J'),	
    path('modeloIIC', T1ModeloItemItemC.as_view(), name='t1_modeloII_C'),
    path('modeloIIP', T1ModeloItemItemP.as_view(), name='t1_modeloII_P'),
	
    
    ] 