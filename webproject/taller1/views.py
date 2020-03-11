from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context

from taller1.forms import T1LoginForm, Userid_ProfileForm, Userid_TimestampForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views import View

from django.core.paginator import Paginator

from taller1.models import Userid_Profile, Userid_Timestamp, Userid_NUserId

from taller1.algoritmosJUU import IndiceJaccardUU
from taller1.algoritmosC import SimilitudCoseno
from taller1.algoritmosP import CorrelacionPearson
from taller1.algoritmosJII import IndiceJaccardII
from taller1.algoritmosCII import SimilitudCosenoII
from taller1.algoritmosPII import CorrelacionPearsonII

from taller1.algoritmoCoseno import Coseno

class T1ModeloUserUserJ(View):
    template_name='taller1/modeloUsuarioJ.html'
    
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            ij = IndiceJaccardII()
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            #userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            #userCode = userCode[0].n_userid
            #print("userid=",userid, " userCode=", userCode)
            print("userid=", userid)
			
            lista_similares_jaccard={}
            #lista_similares_jaccard =  IndiceJaccardUU.listaUsuariosSimilares(self, userid)
            lista_similares_jaccard = ij.items_most_similar(userid)
            
            return render(request, self.template_name, {'usuario_activo':userProfile, 'lista_similares_jaccard':lista_similares_jaccard})
			
        else:
            return redirect('t1_login')
			
class T1ModeloUserUserC(View):
    template_name='taller1/modeloUsuarioC.html'
    
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            userCode = userCode[0].n_userid
            print("userid=",userid, " userCode=", userCode)            
           
            lista_similares_cosine={}
               
            resp = Coseno.recomendacionUsuario(self,userid)
            print(resp)
            lista_similares_cosine=resp['lista_coseno_usuario']
            lista_recomendacion=resp['lista_recomendacion']            
            print(lista_similares_cosine)
            print(lista_recomendacion)
            
            return render(request, self.template_name, {'usuario_activo':userProfile,'lista_recomendacion':lista_recomendacion,'lista_similares_cosine':lista_similares_cosine})
        else:
            return redirect('t1_login')
        
    
class T1ModeloUserUserP(View):
    template_name='taller1/modeloUsuarioP.html'
    
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            userCode = userCode[0].n_userid
            print("userid=",userid, " userCode=", userCode)
            
            lista_similares_pearson={}
           # lista_similares_pearson = CorrelacionPearson.listaUsuariosSimilares(self,userProfile,perfiles)
        
            return render(request, self.template_name, {'usuario_activo':userProfile,'lista_similares_pearson':lista_similares_pearson})
        else:
            return redirect('t1_login')
			
class T1ModeloItemItemJ(View):
    template_name='taller1/modeloItemJ.html'
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            ij = IndiceJaccardUU()
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            #userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            #serCode = userCode[0].n_userid
            #print("userid=",userid, " userCode=", userCode)
            print("userid=", userid)
            lista_similares_jaccard = {}
            #lista_similares_jaccard = IndiceJaccardII.listaItemsSimilares(self, userCode)
            lista_similares_jaccard = ij.items_most_similar(userid)
            
            return render(request, self.template_name, {'usuario_activo':userProfile, 'lista_similares_jaccard':lista_similares_jaccard})
           
        else:
            return redirect('t1_login')

class T1ModeloItemItemC(View):
    template_name='taller1/modeloItemC.html'
    
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            userCode = userCode[0].n_userid
            print("userid=",userid, " userCode=", userCode)
            
            lista_similares_cosine={}
               
            resp = Coseno.recomendacionItem(self,userid)
            print(resp)
            lista_similares_cosine=resp['lista_coseno_artista']
            lista_artista=resp['artista_activo']            
            print(lista_similares_cosine)
            print(lista_artista)
            
            return render(request, self.template_name, {'usuario_activo':userProfile,'lista_artista':lista_artista,'lista_similares_cosine':lista_similares_cosine})
           
        else:
            return redirect('t1_login')
			

class T1ModeloItemItemP(View):
    template_name='taller1/modeloItemP.html'
    def get(self, request, *args, **kwargs):        
        userid = request.session.get('usuario_activo')
        if userid:
            userProfile = Userid_Profile.objects.get(pk=userid)
            
            userCode = list(Userid_NUserId.objects.filter(userid__in=[userid]))
            
            userCode = userCode[0].n_userid
            print("userid=",userid, " userCode=", userCode)
            
            lista_similares_pearson={}
            
            return render(request, self.template_name, {'usuario_activo':userProfile,'lista_similares_pearson':lista_similares_pearson})
        else:
            return redirect('t1_login')
			
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
            iteracciones_list = Userid_Timestamp.objects.filter(userid_Profile=userProfile)[:100]
            print("iteracciones_list=",iteracciones_list.count())
            paginator = Paginator(list(iteracciones_list), 20)
            page_number = request.GET.get('page')
            iteracciones = paginator.get_page(page_number)
            return render(request,'taller1/perfil.html',{'usuario':userProfile,'page_obj':iteracciones})
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
            userNuser = Userid_NUserId()            
            userNuser.userid = nuevo['userid'].value()
            userNuser.n_userid = userNuser.incrementNumber()
            print("userNuser=",userNuser)
            userNuser.save()
			
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
            
            