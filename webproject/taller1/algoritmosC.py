from taller1.models import Userid_Profile, Userid_ProfileCalculado

import pandas as  pd
from collections import defaultdict
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from django.db import connection
import pandas as pd
import numpy as np
import math

class SimilitudCoseno():
    def listaItemsSimilares(self,usuario_activo):
        
        
        cantidad = 10
        
        lista_similares=[]    
        udata={}      
        #udata = SimilitudCoseno.cargarDatosUserTimeStamp(self)   
        ratingsbyuser1={}
        #ratingsbyuser1 = SimilitudCoseno.cargarDatosRatings(self)
        #predictions = SimilitudCoseno.cargarDatospredictions(self)
        
        #lista_similares = SimilitudCoseno.listaRecomendacionCosenoItem(self,usuario_activo,udata,ratingsbyuser1,predictions,cantidad)
        
        lista_similares = SimilitudCoseno.buscarListaPrediccion(self,usuario_activo)       
                
        return lista_similares
        
    def buscarDatoArtistaTimeStamp(self, art_id):
        udata = pd.read_sql_query('''select distinct ("ut"."codigo1") as "artid", "ut"."artist" as "artname"
                    from taller1_userid_timestamp as ut, 
                    taller1_userid_nuserid as un, 
                    taller1_artist_nartist as a
                    where "ut"."userid_Profile_id"= "un"."userid"
                    and "ut"."codigo1"= "a"."artist"
                    and "a"."n_artist" ='''+art_id+'''; ''', connection)
        return udata

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

    
    def buscarListaPrediccion(self, usuario_activo):
        sql='''select distinct ("ut"."artist")
                    from "taller1_userid_timestamp" as "ut", "taller1_artist_nartist" as "a"
                    where "ut"."codigo1" = "a"."artist"
                    and  "a"."n_artist" in (
                    select "art_id"
                    from taller1_userid_rating
                    where "art_id" in (
                    select "art_id" 
                    from "taller1_pred_coseno_ii"
                    where "user_id"= %i
                    order by "est")
                    order by "rating" desc
                    limit 10);''' %(usuario_activo)
        lista_prediccion = pd.read_sql_query(sql, connection)
        return lista_prediccion
    
    def cargarDatosRatings(self):
        ratingsbyuser1 = pd.read_sql_query('''SELECT * FROM taller1_userid_rating LIMIT 5000;''', connection)
        ratingsbyuser1 = ratingsbyuser1[['user_id','art_id','count','rating']]
        return ratingsbyuser1 
    
    def cargarDatospredictions(self):
        predictions =pd.read_sql_query('''SELECT  "user_id", "art_id", "est" FROM taller1_pred_coseno_ii LIMIT 50000;''', connection)
        predictions = predictions.sort_values(by='est', ascending=False)
        return predictions
    
    def listaRecomendacionCosenoItem(self,userid,udata,ratingsbyuser1,predictions,N):
        #la coleccion predictions deb estar ordenada de mayor a menor
        pred = predictions.loc[predictions.user_id == userid]
        pred = pred[:N]
        lista = []
        for i,d in pred.iterrows():
            artid = d['art_id']
            # LA siguiente linea creo no hace nada 
            #artid = ratingsbyuser1.loc[ratingsbyuser1.art_id==artid,'art_id'].iloc[0]
            #buscar en los datos orinales (udata) el nombre de este artid
            try:
                lista.append(SimilitudCoseno.buscarDatoArtistaTimeStamp(self,artid))
                #lista.append(udata.loc[udata.artid==artid,'artname'][0])
            except:
                print("Coseno Item, No encontro artista=",artid)        
        return lista
                
