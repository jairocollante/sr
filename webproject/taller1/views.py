from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context

from taller1.forms import T1LoginForm, Userid_ProfileForm, Userid_TimestampForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views import View

from taller1.models import Userid_Profile, Userid_Timestamp

class T1ModeloUserUser(View):
    template_name='taller1/modeloUsuario.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
	
class T1ModeloItemItem(View):
    template_name='taller1/modeloItem.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    
class T1LoginView(FormView):
    template_name='taller1/login.html'
    form_class= T1LoginForm
    initial = {'key': 'value'}
    sucess_url='/t1_perfil/'
    key_cookie = 'usuario_activo'    
    
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
            print("userProfile=",userProfile)
            
            request.session['usuario_activo']=userProfile.userid

            iteracciones = Userid_Timestamp.objects.filter(userid_Profile=userProfile)
            print("iteracciones=",iteracciones.count())
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
    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            iteracciones = Userid_Timestamp.objects.filter(userid_Profile=userProfile)
            print("iteracciones=",iteracciones.count())
            return render(request,'taller1/perfil.html',{'usuario':userProfile,'iteracciones':iteracciones})
        else:
            return redirect('t1_login')

        
class T1Userid_ProfileList(ListView):
    model = Userid_Profile

class T1Userid_ProfileFormView(FormView):
    form_class = Userid_ProfileForm
    initial = {'key': 'value'}
    template_name='taller1/nuevoUsuario.html'
    sucess_url='/t1_login/'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
		
    def form_valid(self, form):
        return super().form_valid(form)
		
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo = Userid_ProfileForm(request.POST)
            nuevo.save()
            return redirect('t1_login') 
        else:
            return render(request, self.template_name, {'form': form})

class T1Userid_TimestampFormView(FormView):
    form_class = Userid_TimestampForm
    initial = {'key': 'value'}
    template_name='taller1/nuevoIteraccion.html'
    sucess_url='t1_login'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
		
    def form_valid(self, form):
        return super().form_valid(form)
		
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo = Userid_TimestampForm(request.POST)
            nuevo.save()
            return redirect('t1_login')
        else:
            return render(request, self.template_name, {'form': form})
            
            