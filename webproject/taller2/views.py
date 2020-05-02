from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views import View

from taller2.forms import T2LoginForm
from taller2.models import User, Review

class T2Hibrido(View):
    template_name='taller2/T2Hibrido.html'
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            print("userid=", userid)
        else:
            return redirect('t2_login')

class T2LoginView(FormView):
    template_name='taller2/login.html'
    form_class= T2LoginForm
    initial = {'key': 'value'}
    sucess_url='/t2_perfil/'
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
            print("userProfile=", userProfile)
            
            request.session['usuario_activo']=userProfile.user_id

            interacciones = Review.objects.filter(user_id=userProfile)
            print("interacciones=",interacciones.count())
            return render(request,'taller2/perfil.html',{'usuario':userProfile, 'interacciones':interacciones})
    
    def form_valid(self, form):
        form.doLogin()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("contexto")
        context['usuario_activo'] = self.form_class(request.POST)
        return context

class T2PerfilView(View):
    template_name='taller2/perfil.html'
    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            iteracciones_list = Userid_Timestamp.objects.filter(userid_Profile=userProfile)[:100]
            print("iteracciones_list=",iteracciones_list.count())
            paginator = Paginator(list(iteracciones_list), 20)
            page_number = request.GET.get('page')
            iteracciones = paginator.get_page(page_number)
            return render(request,'taller1/perfil.html',{'usuario':userProfile,'page_obj':iteracciones})
        else:
            return redirect('t1_login')

class T1Userid_ProfileList(ListView):
    model = User
    paginate_by = 100