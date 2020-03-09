from taller1.models import Userid_Profile, Userid_ProfileCalculado

import pandas as  pd
from collections import defaultdict
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine


from django.db import connection

#
class IndiceJaccard():
    
    def listaUsuariosSimilares(self,usuario_activo):
        
        cantidad = 10
        
        lista_similares=[]          
        udata = IndiceJaccard.cargarDatosUserTimeStamp(self)     
        ratingsby = udata.groupby(['user_id','art_id','artname'])['art_id'].count().reset_index(name='count')
                        
        usersPerItem = defaultdict(set)
        itemsPerUser =defaultdict(set)
        itemNames={}
        
        for i,d in ratingsby.iterrows():
            user,item = d['user_id'], d['art_id']
            usersPerItem[item].add(user)
            itemsPerUser[user].add(item)
            itemNames[item] = d['artname']        
        
        lista_similares = IndiceJaccard.rs_user_user_jaccard(self,usuario_activo,usersPerItem,itemsPerUser,itemNames,cantidad)
        
        return lista_similares[:cantidad]
    
    def listaItemsSimilares(self,usuario_activo):
        
        cantidad =10
        
        lista_similares=[]  
        udata = IndiceJaccard.cargarDatosUserTimeStamp(self)     
        ratingsby = udata.groupby(['user_id','art_id','artname'])['art_id'].count().reset_index(name='count')
                        
        usersPerItem = defaultdict(set)
        itemsPerUser =defaultdict(set)
        itemNames={}
        
        for i,d in ratingsby.iterrows():
            user,item = d['user_id'], d['art_id']
            usersPerItem[item].add(user)
            itemsPerUser[user].add(item)
            itemNames[item] = d['artname']        
        
        lista_similares = IndiceJaccard.rs_user_item_jaccard(self,usuario_activo,usersPerItem,itemsPerUser,itemNames,cantidad)
                
        return lista_similares[:cantidad]
    
    def cargarDatosUserTimeStamp(self):
        udata = pd.read_sql_query('''select "ut"."userid_Profile_id" as "userid","ut"."c_timestamp" as "timestamp"
                    ,"ut"."codigo1" as "artid", "ut"."artist" as "artname", "ut"."codigo2" as "traid","ut"."song" as "traname"
                    , "un"."n_userid" as "user_id","a"."n_artist" as "art_id"
                    from taller1_userid_timestamp as ut, 
                    taller1_userid_nuserid as un, 
                    taller1_artist_nartist as a
                    where "ut"."userid_Profile_id"= "un"."userid"
                    and "ut"."codigo1"= "a"."artist"
                    limit 10000; ''', connection)
        return udata
    
    def cargarDatosRatings(self):
        ratingsbyuser1 = pd.read_sql_query('''SELECT * FROM taller1_userid_rating LIMIT 1000;''', connection)
        ratingsbyuser1 = ratingsbyuser1[['user_id','art_id','count','rating']]
        ratingsbyuser1 =ratingsbyuser1.dropna()
        return ratingsbyuser1    
    
        
    def Jaccard(self,s1,s2):
        number = len(s1.intersection(s2))
        denom =  len(s1.union(s2))
        return number/denom       
        
    # retorna los 10 items mas similares al item i en funcion a la similitud jaccard de los usurios que  han escuchado el item i
    def mostSimilar_item(self,i,usersPerItem,n):
        similares=[]
        users =  usersPerItem[i]
        for i2 in  usersPerItem:
            if i2==i:continue
            sim = IndiceJaccard.Jaccard(self,users,  usersPerItem[i2])
            similares.append((sim,i2))
        similares.sort(reverse=True)
        return similares[:n]
    
    # dado un usuario retorna los 10 usuarios mas similares al usuario i en funcion a la similitud jaccard de los items que estos usuarios consumieron
    def mostSimilar_usuario(self,i,itemsPerUser,n):
        similares=[]
        items =  itemsPerUser[i]
        for u2 in  itemsPerUser:
            if u2==i:continue
            sim = IndiceJaccard.Jaccard(self,items,  itemsPerUser[u2])
            similares.append((sim,u2))
        similares.sort(key=lambda t: t[0],reverse= True)
        return similares[:n]
    
    #retorna los Items que No ha consumido un usuario de una lista de items
    def items_no_in_usuario(self,items,items_u):
        items_ok =[]
        for item in items:
            if item[1] not in items_u:
                items_ok.append(item)
        return items_ok
    
    #retorna los Items que No ha consumido un usuario de una lista de items
    def items_no_in_usuario_lista(self,items,items_u):
        items_ok =[]
        for item in items:
            if item not in items_u:
                items_ok.append(item)
        return items_ok
    
    # dado un usuario recomenida items que no ha consumido en funcion de la similitud jaccard a items que han consumido otros usuarios
    def rs_user_item_jaccard(self,userid,usersPerItem,itemsPerUser,itemNames,n):
        lista_items = itemsPerUser[userid]
        items_similares =[]
        for item in lista_items:
            items_similares = items_similares + (IndiceJaccard.mostSimilar_item(self,item,usersPerItem,n))
            items_similares = IndiceJaccard.items_no_in_usuario(self,items_similares,lista_items)
            items_similares.sort(reverse=True)
            
        lista_resultante=[]
        for i in items_similares:
            lista_resultante.append(itemNames[i])
        
        return lista_resultante
    
    # dado un usuario recomenida items que no ha consumido en funcion de la similitud jaccard a usuarios que han consumido estos items
    def rs_user_user_jaccard(self,userid,usersPerItem,itemsPerUser,itemNames,n):     
        
        lista_items = itemsPerUser[userid]
        lista_usuarios = IndiceJaccard.mostSimilar_usuario(self,userid,itemsPerUser,n)
        items_similares = set()
        items_similares_ =[]
        for user in lista_usuarios:
            for item in itemsPerUser[user[1]]:
                items_similares.add(item)
            items_similares_ = IndiceJaccard.items_no_in_usuario_lista(self,items_similares,lista_items)
            if len(items_similares_) >= n:
                break
        
        lista_resultante=[]
        for i in items_similares_:
            lista_resultante.append(itemNames[i])
            
        return lista_resultante

import pandas as pd
import numpy as np
import math

class SimilitudCoseno():
    def listaUsuariosSimilares(self,usuario_activo,perfiles):
        lista_similares=[]
        
        df_perfiles = pd.DataFrame(list(perfiles.values()))         
        
        genderNumber =  SimilitudCoseno.transforGender(self,df_perfiles) 
        countryNumber = SimilitudCoseno.transforCountry(self,df_perfiles)       
        
        df_perfiles = SimilitudCoseno.procesarDatos(self,df_perfiles,genderNumber,countryNumber)    
        
        df_usuario_activo= pd.DataFrame(data=[[usuario_activo.userid, usuario_activo.gender ,usuario_activo.age,usuario_activo.country ,usuario_activo.registered ,genderNumber[usuario_activo.gender],countryNumber[usuario_activo.country] ]], columns=df_perfiles.columns)            
              
        
        for index, usuario_comparado in df_perfiles.iterrows():
            if(len(lista_similares)==10):
                return lista_similares
            if(usuario_activo.userid == usuario_comparado.userid):
                continue
            
            cosine  = SimilitudCoseno.calcularUsuarioPerfil(self,df_usuario_activo, usuario_comparado)
            usuario_calculado = Userid_ProfileCalculado()
            usuario_calculado.userid_profile = Userid_Profile()
            usuario_calculado.userid_profile.userid = usuario_comparado.get(key='userid')
            usuario_calculado.userid_profile.gender = usuario_comparado.get(key='gender')
            usuario_calculado.userid_profile.age = usuario_comparado.get(key='age')
            usuario_calculado.userid_profile.country = usuario_comparado.get(key='country')
            usuario_calculado.userid_profile.registered = usuario_comparado.get(key='registered')
            usuario_calculado.cosine = cosine
            lista_similares.append(usuario_calculado)
            
        lista_similares = sorted(lista_similares,key =Userid_ProfileCalculado.similarityCosine, reverse = True)
        return lista_similares
        
    def calcularUsuarioPerfil(self,df_usuario_activo, usuario_comparado):
        df_usuario_comparado = pd.DataFrame([usuario_comparado],columns=df_usuario_activo.columns)
        
        pg = int(df_usuario_activo.genderN)  * int(df_usuario_comparado.genderN)
        pa=0
        if  df_usuario_activo.age.size >1 :
            if df_usuario_comparado.age.size >1 :
                pa = int(df_usuario_activo.age)      * int(df_usuario_comparado.age)
        pc = int(df_usuario_activo.countryN) * int(df_usuario_comparado.countryN)
        
        
        cg_a = int(df_usuario_activo.genderN)  * int(df_usuario_activo.genderN)
        ca_a=0
        if df_usuario_activo.age.size >1 :
            if df_usuario_comparado.age.size >1 :
                ca_a = int(df_usuario_activo.age)      * int(df_usuario_activo.age)
        cc_a = int(df_usuario_activo.countryN) * int(df_usuario_activo.countryN)
        
        
        m_a = math.sqrt(cg_a+ca_a+cc_a)
        
        cg_c = int(df_usuario_comparado.genderN)  * int(df_usuario_comparado.genderN)
        ca_c=0
        if df_usuario_activo.age.size >1 :
            if df_usuario_comparado.age.size >1 :
                ca_c = int(df_usuario_comparado.age)      * int(df_usuario_comparado.age)
        cc_c = int(df_usuario_comparado.countryN) * int(df_usuario_comparado.countryN)
        
        m_c = math.sqrt(cg_c+ca_c+cc_c)
        
        cosine =(pg+pa+pc)/(m_a * m_c)
        
        return cosine
    
    def transforCountry(self,df_perfiles):
        cu = df_perfiles.country.unique()        
        ol = {}
        i=1
        for c in cu:
            ol[c]=i
            i=i+1
            
        return ol
    
    def transforGender(self,df_perfiles):
        gu = df_perfiles.gender.unique()        
        ol = {}
        i=1
        for g in gu:
            ol[g]=i
            i=i+1
            
        return ol
        
    
    def procesarDatos(self,df_perfiles,genderNumber, countryNumber):  
        
        df_perfiles['genderN'] = [genderNumber[g] for g in df_perfiles.gender]  
        
        df_perfiles['countryN']=[countryNumber[c] for c in df_perfiles.country] 
        
        return df_perfiles


from scipy.stats import pearsonr

class CorrelacionPearson():
    def listaUsuariosSimilares(self,usuario_activo,perfiles):
        lista_similares=[]
        
        df_perfiles = pd.DataFrame(list(perfiles.values()))         
        
        genderNumber =  SimilitudCoseno.transforGender(self,df_perfiles) 
        countryNumber = SimilitudCoseno.transforCountry(self,df_perfiles)       
        
        df_perfiles = SimilitudCoseno.procesarDatos(self,df_perfiles,genderNumber,countryNumber)    
        
        df_usuario_activo= pd.DataFrame(data=[[usuario_activo.userid, usuario_activo.gender ,usuario_activo.age,usuario_activo.country ,usuario_activo.registered ,genderNumber[usuario_activo.gender],countryNumber[usuario_activo.country] ]], columns=df_perfiles.columns)            
                      
        for index, usuario_comparado in df_perfiles.iterrows():
            if(len(lista_similares)==10):
                return lista_similares
            if(usuario_activo.userid == usuario_comparado.userid):
                continue
            
            pearson  = CorrelacionPearson.calcularUsuarioPerfil(self,df_usuario_activo, usuario_comparado)
            usuario_calculado = Userid_ProfileCalculado()
            usuario_calculado.userid_profile = Userid_Profile()
            usuario_calculado.userid_profile.userid = usuario_comparado.get(key='userid')
            usuario_calculado.userid_profile.gender = usuario_comparado.get(key='gender')
            usuario_calculado.userid_profile.age = usuario_comparado.get(key='age')
            usuario_calculado.userid_profile.country = usuario_comparado.get(key='country')
            usuario_calculado.userid_profile.registered = usuario_comparado.get(key='registered')
            usuario_calculado.pearson = pearson
            lista_similares.append(usuario_calculado)            
        lista_similares = sorted(lista_similares,key = Userid_ProfileCalculado.correlacionPearson, reverse = True)
        
        return lista_similares

    def calcularUsuarioPerfil(self,df_usuario_activo, usuario_comparado):
        df_usuario_comparado = pd.DataFrame([usuario_comparado],columns=df_usuario_activo.columns)
        
        #Rellenar valores vacio        
        
        if str(df_usuario_activo.age.values[0]) =='' or str(df_usuario_activo.age.values[0]) =='nan':
            df_usuario_activo.age=0
        
        if str(df_usuario_comparado.age.values[0]) == '' or str(df_usuario_comparado.age.values[0])=='nan':
            df_usuario_comparado.age=0        
        
        ua = np.array([df_usuario_activo.genderN.values[0],   df_usuario_activo.age.values[0],    df_usuario_activo.countryN.values[0]])
        uc = np.array([df_usuario_comparado.genderN.values[0],df_usuario_comparado.age.values[0], df_usuario_comparado.countryN.values[0]])
        corr, _ = pearsonr(ua, uc)
        return corr
                
