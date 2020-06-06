from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.forms import formset_factory

from taller3.forms import T3LoginForm, T3UserForm, T3SearchForm, T3RatingForm
from taller3.models import User

from py2neo import Graph, Node, NodeMatcher
import connexion

import json

# Create your views here.
class T3RecommenderView(View):
    template_name='taller3/recommendation.html'
    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            #userProfile = User.objects.using('db_t3').get(user_id=userid)
            #data = FiltroColaborativo.getRecCollab(self, f'User {userid}', 10)
            '''
            mijson = data.to_json(orient='records')
            respjson = json.loads(mijson) 
            '''
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            userId = f'User {userid}'
            n = 10
            print ("Usuario " + userId)
            
            rec = graph.run('MATCH (u1:User {id:$userid})-[r:RATED]->(m:Movie) '
                            'WITH u1, avg(r.rating) AS u1_mean '
                            'MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2) '
                            'WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10 '
                            'MATCH (u2)-[r:RATED]->(m:Movie) '
                            'WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings '
                            'UNWIND ratings AS r '
                            'WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom, '
                            'sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom, u1, u2 WHERE denom <> 0 '
                            'WITH u1, u2, nom/denom AS pearson '
                            'ORDER BY pearson DESC LIMIT 10 '
                            'MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) ) '
                            'RETURN m.title AS title, SUM( pearson * r.rating) AS score '
                            'ORDER BY score DESC LIMIT toInteger($n);', userid=userId, n=n)
            '''
            rec = graph.run('MATCH (u:User {id: $userId})-[r:RATED ]->(movies) RETURN movies.title AS movie, r.rating AS rating', userId=userId)                            
            '''
            data=rec.data()
            #data = []
            #for record in rec:
            #  data.append({'title': record['title'], 'score': record['score']})

            #data = json.dumps(rec.data()) # después de copiar, rec.data() devuelve vacio, es un cursor
            return render(request, self.template_name,{'usuario_activo':userId, 'resp':data})
        else:
            return redirect('t3_login')

    def post(self, request, *args, **kwargs):
        print("post")

class T3MoviesView(View):
    template_name='taller3/movies.html'
    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            userId = f'User {userid}'
            print ("Usuario " + userId)
            
            rec = graph.run('MATCH (u:User {id: $userId})-[r:RATED ]->(movies) RETURN movies.title AS movie, r.rating AS rating', userId=userId)                            
            data=rec.data()
            return render(request, self.template_name,{'usuario_activo':userId, 'resp':data})
        else:
            return redirect('t3_login')

    def post(self, request, *args, **kwargs):
        print("post")

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
    
class T3UserFormView(FormView):
    form_class = T3UserForm
    initial = {'key': 'value'}
    template_name='taller3/newUser.html'
    sucess_url='login'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
        
      
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save(using='db_t3')
            
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            sql = 'CREATE (u:User {id:\''+str(obj.user_id)+'\'}) return u'
            rec = graph.run(sql)                    
            data=rec.data()
            
            return redirect('t3_login')
            
        else:
            return render(request, self.template_name, {'form': form})
        
class T3SearchFormView(FormView):
    form_class = T3SearchForm
    initial = {'key': 'value'}
    template_name='taller3/search.html'
    sucess_url='t3_found'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
        
      
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            print('buscar=',text )
            
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            sql = 'MATCH (m:Movie) where toLower(m.title) =~\'.*'+text+'.*\' return m.title as movie_title, m.id as movie_id'
            print(sql)
            rec = graph.run(sql)                    
            data=rec.data()
            
            print(data)
            
            initial= [{'title':'Rapido y furioso','id':'1212'},{'title':'Pelicula 2','id':'1554'}]
            
            form = T3RatingForm(initial = initial)
            
            ratingFormSet = formset_factory(form)
            
            
            return render(request, 'taller3/found.html', {'form': ratingFormSet})
            
                    
            
class T3FoundFormView(FormView):
    form_class = T3RatingForm
    initial = {'key': 'value'}
    template_name='taller3/found.html'
    sucess_url='found'
    
    def get(self, request, *args, **kwargs):
        movies = kwargs.movies
        print(movies)
        form = self.form_class(initial=self.initial)
        ratingFormSet = formset_factory(form)
        
        
        return render(request, self.template_name, {'form': ratingFormSet})
        
      
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            print('buscar=',text )
            
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            sql = 'MATCH (m:Movie) where toLower(m.title) =~\'.*'+text+'.*\' return m.title as movie_title, m.id as movie_id'
            print(sql)
            rec = graph.run(sql)                    
            data=rec.data()
            
            print(data)
            
            return render(request, self.template_name,{'resp':data})
