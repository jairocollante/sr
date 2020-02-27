from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context

from taller1.forms import T1LoginForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views import View

from taller1.models import Userid_Profile, Userid_Timestamp

# Create your views here.
    
class T1LoginView(FormView):
    template_name='taller1/login.html'
    form_class= T1LoginForm
    initial = {'key': 'value'}
    sucess_url='/t1_perfil/'
    context_object_name = 'usuario_activo'    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.doLogin()
            if usuario.count() == 0:
                return render(request,self.template_name, {'form': form,'titulo': 'Usuario no existe'})
            userProfile = usuario[0]
            print("userProfile",userProfile)
            iteracciones = Userid_Timestamp.objects.filter(userid_Profile=userProfile)
            return render(request,'taller1/perfil.html',{'usuario':userProfile, 'iteracciones':iteracciones})
        return render(request, self.template_name, {'form': form})
    
    def form_valid(self, form):
        form.doLogin()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("contexto")
        context['usuario_activo'] = self.form_class(request.POST)
        return context
        
class T1PerfilView(View):
    template_name='taller1/perfil.html'
    form_class= Userid_Profile
    print("T1PerfilView")
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {'usuario': usuario})
        
class Userid_ProfileList(ListView):
    model = Userid_Profile
