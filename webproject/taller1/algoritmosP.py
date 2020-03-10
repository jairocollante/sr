from taller1.models import Userid_Profile, Userid_ProfileCalculado

import pandas as  pd
from collections import defaultdict
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import math
from scipy.stats import pearsonr
from django.db import connection

#

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
                
