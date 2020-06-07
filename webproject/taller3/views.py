from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.forms import formset_factory

from taller3.forms import T3LoginForm, T3UserForm, T3SearchForm, T3RatingForm
from taller3.models import User

from py2neo import Graph, Node, NodeMatcher,Relationship
import connexion

import pandas as pd
from scipy.spatial import distance

import json

# Create your views here.
class T3RecommenderView(View):
    template_name='taller3/recommendation.html'
    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            userId = f'User {userid}'
            n = 10
            n2 = n * 2
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
            data = rec.data()
            data2 = self.get_full_recomendacion_user(graph, userId, n2, 5, 2, "DIRECTED", "ACTED")

            for recomendacion in data2:
                data.append(recomendacion)
                if (len(data) >= n2):
                    break;

            return render(request, self.template_name,{'usuario_activo':userId, 'resp':data})
        else:
            return redirect('t3_login')

    def post(self, request, *args, **kwargs):
        print("post")

    def get_items_user(self, graph, user):
        busca_items = "MATCH (User {id:'%s'})-[r:RATED]->(n) RETURN n.title, r.rating" % user
        return graph.run(busca_items).to_data_frame()   #.to_table()

    def get_similar_users(self, graph, user, n):
        #debe correr gds.alpha.similarity.asVector en NEO4J
        query = """
                MATCH (p1:User {id: '%s'})-[rated1:RATED]->(m)<-[rated2:RATED]-(p2:User) WHERE p2 <> p1
                WITH p1, gds.alpha.similarity.asVector(m, rated1.rating) AS p1Vector, 
                    p2, gds.alpha.similarity.asVector(m, rated2.rating) AS p2Vector 
                RETURN p1.id AS from, 
                    p2.id AS to,  
                    gds.alpha.similarity.pearson(p1Vector, p2Vector, {vectorType: "maps"}) AS similarity 
                ORDER BY similarity DESC;
                """ % user
        
        similar_user = graph.run(query).to_data_frame()
        similar_user = similar_user[similar_user.similarity >0]
        if n > 100:
            similar_user = similar_user[:100]
        else:
            similar_user = similar_user[:n]
        
        return  similar_user

    def get_full_recomendacion_user(self, graph, user, n, k, s, *perfil):
        #get_recomendacion_user(u,n,k,s)
        #u=user activo, n= recomendaciones, k= tamaño vecindario, s=usuario por perfil mas cercanos, perfil=preferencias del usuario
        print("Inicia Recomendacion usuario : " , user)

        recomendacion = [] 
        existentes = []
        user_perfil = self.get_full_perfil_user(graph, user, perfil)
        print("Perfil del Usuario [%s]:" % user)
        for per in user_perfil:
            print(per)
        
        print (self.get_items_user(graph, user))
        user_peliculas = list(self.get_items_user(graph, user)['n.title'])
        
        print("Perfil usuarios similares")
        perfil_similares = self.get_full_perfil_other_user(graph, user, k, perfil)
        print("Se encontro el perfil para ", len(perfil_similares), " Usuarios similares")
        mas_cercanos = self.full_distancia_user_others(graph, user_perfil, perfil_similares, s)
        print("Los ", s, " usuarios mas cercanos :")
        print(mas_cercanos)

        print("Se calculó la distancia de ", len(mas_cercanos), " perfiles mas cercanos")
        
        peliculas_ = []
        for usuario in mas_cercanos:
            for indx,peli in self.get_items_user(graph, usuario[0]).iterrows():
                if peli['n.title'] not in peliculas_:
                    peliculas_.append(peli['n.title'])
        
        for peli in peliculas_:
            if (peli in user_peliculas):
                existentes.append(peli)
                
            if (peli not in user_peliculas) and len(recomendacion) < n:
                recomendacion.append(peli)
        
        print("Se encontraron ", len(peliculas_), " peliculas recomendables")
        print("Peliculas vistas por el usuario ", len(user_peliculas))    
        print("Se encontraron ", len(existentes), " Peliculas vistas por el usuario dentro de las recomendables")
        
#        return recomendacion, existentes
        return recomendacion

    def get_full_perfil_user(self, graph, user, perfil):
        #perfiles = ['DIRECTED', 'ACTED']
        peliculas_user = self.get_items_user(graph, user)
        full_perfil = []
    
        if len(perfil) > 0:
            perfiles =[]
            for i in range(0,len(perfil)):  
                full_perfil.extend(self.get_perfil_user_(graph, peliculas_user, perfil[i]))
        
        return full_perfil

    def get_full_perfil_other_user(self, graph, user, n,perfil):
        dat = self.get_similar_users(graph ,user, n)
        perfiles_other ={}
        for index,other in dat.iterrows():
            user_other = other['to']
            full_perfil =[]
            
            peliculas_user = self.get_items_user(graph, user_other)
            if len(perfil) > 0:
                perfiles =[]
                for i in range(0,len(perfil)):
                    #print(perfil)
                    full_perfil.extend(self.get_perfil_user_(graph, peliculas_user,perfil[i]))
                perfiles_other[user_other] =full_perfil
                
        return perfiles_other
            
    def get_perfil_user_(self, graph, peliculas_user, perfil):
        gene= "MATCH (p:Movie {title:'%s'}) -[:" + perfil +  "]-(g) return g.primaryName"
        
        generos_perfil ={}
        total_gen = 0
        for index,peli in peliculas_user.iterrows():
            rating = float(peli['r.rating']) / 5
            guery_gen = gene % peli['n.title'].replace("'","\\'")
            #print(guery_gen)
            generos_user = graph.run(guery_gen).to_data_frame()
            
            if (generos_user.size <= 0):
                continue
            
            for genuser in generos_user['g.primaryName']:
                total_gen = total_gen +1
                if genuser not in generos_perfil.keys():
                    generos_perfil[genuser]= rating
                else:
                    generos_perfil[genuser] = generos_perfil[genuser] + rating
                    
        generos_perfil.update((x, y/total_gen) for x, y in generos_perfil.items())
        generos_perfil = sorted(generos_perfil.items(), key=lambda x: x[1], reverse=True)
        
        return generos_perfil

    def full_distancia_user_others(self, graph, mi_perfil, others, n):
        distancia ={}
        mis_keys =[]
        mis_valores ={}
        misValores=[]

        for mis_items in mi_perfil:
            if mis_items[0] not in mis_valores:
                mis_valores[mis_items[0]] =  mis_items[1]
                misValores.append(mis_items[1])
            else:
                mis_valores[mis_items[0]] = "*" 

        for k in  others:
            other_valores ={}
            otherValores =[]
            for i in others[k]:
                other_valores[i[0]] = i[1]
            for misk in mis_valores:
                if misk in other_valores:
                    if mis_valores[misk] == "*":
                        mis_valores[misk] = other_valores[misk]
                    otherValores.append(other_valores[misk])
                else:
                    otherValores.append(0)
                    
            dst = distance.euclidean(misValores, otherValores)
            distancia[k] = dst

        distancia = sorted(distancia.items(), key=lambda x: x[1], reverse=False)

        return distancia[:n]

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

class T3RecommenderView2(View):
    template_name='taller3/recommendation.html'

    def get(self, request, *args, **kwargs):
        userid = request.session.get('usuario_activo')
        if userid:
            USERNAME = "neo4j"
            PASS = "Grupo06" #default
            graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
            userId = f'User {userid}'
            n = 10
            print ("Usuario " + userId)
            
            data = self.get_full_recomendacion_user(graph, userId, n, 5, 2, "DIRECTED", "ACTED")
            return render(request, self.template_name, {'usuario_activo':userId, 'resp':data})
        else:
            return redirect('t3_login')

    def post(self, request, *args, **kwargs):
        print("post")

    def get_items_user(self, graph, user):
        busca_items = "MATCH (User {id:'%s'})-[r:RATED]->(n) RETURN n.title, r.rating" % user
        return graph.run(busca_items).to_data_frame()   #.to_table()

    def get_similar_users(self, graph, user, n):
        #debe correr gds.alpha.similarity.asVector en NEO4J
        query = """
                MATCH (p1:User {id: '%s'})-[rated1:RATED]->(m)<-[rated2:RATED]-(p2:User) WHERE p2 <> p1
                WITH p1, gds.alpha.similarity.asVector(m, rated1.rating) AS p1Vector, 
                    p2, gds.alpha.similarity.asVector(m, rated2.rating) AS p2Vector 
                RETURN p1.id AS from, 
                    p2.id AS to,  
                    gds.alpha.similarity.pearson(p1Vector, p2Vector, {vectorType: "maps"}) AS similarity 
                ORDER BY similarity DESC;
                """ % user
        
        similar_user = graph.run(query).to_data_frame()
        similar_user = similar_user[similar_user.similarity >0]
        if n > 100:
            similar_user = similar_user[:100]
        else:
            similar_user = similar_user[:n]
        
        return  similar_user

    def get_full_recomendacion_user(self, graph, user, n, k, s, *perfil):
        #get_recomendacion_user(u,n,k,s)
        #u=user activo, n= recomendaciones, k= tamaño vecindario, s=usuario por perfil mas cercanos, perfil=preferencias del usuario
        print("Inicia Recomendacion usuario : " , user)

        recomendacion = [] 
        existentes = []
        user_perfil = self.get_full_perfil_user(graph, user, perfil)
        print("Perfil del Usuario [%s]:" % user)
        for per in user_perfil:
            print(per)
        
        print (self.get_items_user(graph, user))
        user_peliculas = list(self.get_items_user(graph, user)['n.title'])
        
        print("Perfil usuarios similares")
        perfil_similares = self.get_full_perfil_other_user(graph, user, k, perfil)
        print("Se encontro el perfil para ", len(perfil_similares), " Usuarios similares")
        mas_cercanos = self.full_distancia_user_others(graph, user_perfil, perfil_similares, s)
        print("Los ", s, " usuarios mas cercanos :")
        print(mas_cercanos)

        print("Se calculó la distancia de ", len(mas_cercanos), " perfiles mas cercanos")
        
        peliculas_ = []
        for usuario in mas_cercanos:
            for indx,peli in self.get_items_user(graph, usuario[0]).iterrows():
                if peli['n.title'] not in peliculas_:
                    peliculas_.append(peli['n.title'])
        
        for peli in peliculas_:
            if (peli in user_peliculas):
                existentes.append(peli)
                
            if (peli not in user_peliculas) and len(recomendacion) < n:
                recomendacion.append(peli)
        
        print("Se encontraron ", len(peliculas_), " peliculas recomendables")
        print("Peliculas vistas por el usuario ", len(user_peliculas))    
        print("Se encontraron ", len(existentes), " Peliculas vistas por el usuario dentro de las recomendables")
        
#        return recomendacion, existentes
        return recomendacion

    def get_full_perfil_user(self, graph, user, perfil):
        #perfiles = ['DIRECTED', 'ACTED']
        peliculas_user = self.get_items_user(graph, user)
        full_perfil = []
    
        if len(perfil) > 0:
            perfiles =[]
            for i in range(0,len(perfil)):  
                full_perfil.extend(self.get_perfil_user_(graph, peliculas_user, perfil[i]))
        
        return full_perfil

    def get_full_perfil_other_user(self, graph, user, n,perfil):
        dat = self.get_similar_users(graph ,user, n)
        perfiles_other ={}
        for index,other in dat.iterrows():
            user_other = other['to']
            full_perfil =[]
            
            peliculas_user = self.get_items_user(graph, user_other)
            if len(perfil) > 0:
                perfiles =[]
                for i in range(0,len(perfil)):
                    #print(perfil)
                    full_perfil.extend(self.get_perfil_user_(graph, peliculas_user,perfil[i]))
                perfiles_other[user_other] =full_perfil
                
        return perfiles_other
            
    def get_perfil_user_(self, graph, peliculas_user, perfil):
        gene= "MATCH (p:Movie {title:'%s'}) -[:" + perfil +  "]-(g) return g.primaryName"
        
        generos_perfil ={}
        total_gen = 0
        for index,peli in peliculas_user.iterrows():
            rating = float(peli['r.rating']) / 5
            guery_gen = gene % peli['n.title'].replace("'","\\'")
            #print(guery_gen)
            generos_user = graph.run(guery_gen).to_data_frame()
            
            if (generos_user.size <= 0):
                continue
            
            for genuser in generos_user['g.primaryName']:
                total_gen = total_gen +1
                if genuser not in generos_perfil.keys():
                    generos_perfil[genuser]= rating
                else:
                    generos_perfil[genuser] = generos_perfil[genuser] + rating
                    
        generos_perfil.update((x, y/total_gen) for x, y in generos_perfil.items())
        generos_perfil = sorted(generos_perfil.items(), key=lambda x: x[1], reverse=True)
        
        return generos_perfil

    def full_distancia_user_others(self, graph, mi_perfil, others, n):
        distancia ={}
        mis_keys =[]
        mis_valores ={}
        misValores=[]

        for mis_items in mi_perfil:
            if mis_items[0] not in mis_valores:
                mis_valores[mis_items[0]] =  mis_items[1]
                misValores.append(mis_items[1])
            else:
                mis_valores[mis_items[0]] = "*" 

        for k in  others:
            other_valores ={}
            otherValores =[]
            for i in others[k]:
                other_valores[i[0]] = i[1]
            for misk in mis_valores:
                if misk in other_valores:
                    if mis_valores[misk] == "*":
                        mis_valores[misk] = other_valores[misk]
                    otherValores.append(other_valores[misk])
                else:
                    otherValores.append(0)
                    
            dst = distance.euclidean(misValores, otherValores)
            distancia[k] = dst

        distancia = sorted(distancia.items(), key=lambda x: x[1], reverse=False)

        return distancia[:n]

