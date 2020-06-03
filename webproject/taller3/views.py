from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from taller3.forms import T3LoginForm
from taller3.models import User

# Create your views here.
class T3RecommenderView(View):
    template_name='taller3/recommendation.html'
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            print("userid=", userid)
            userProfile = User.objects.using('db_t3').get(user_id=userid)
            
            return render(request,self.template_name,{'usuario_activo':userProfile})
        else:
            return redirect('t3_login')


class T3LoginView(FormView):
    template_name='taller3/login.html'
    form_class= T3LoginForm
    initial = {'key': 'value'}
    sucess_url=''
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
            
            request.session['usuario_activo'] = userProfile.user_id

            
            return render(request,'taller3/index.html',{'usuario':userProfile})
    
    def form_valid(self, form):
        form.doLogin()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        print("contexto")
        context['usuario_activo'] = self.form_class(request.POST)
        return context
