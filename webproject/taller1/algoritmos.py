from taller1.models import Userid_Profile, Userid_ProfileCalculado


class IndiceJaccard():
    
    def listaUsuariosSimilares(self,usuario_activo):
        lista_similares=[]
        perfiles = Userid_Profile.objects.todos();
        
        for usuario_comparado in perfiles:
            if(len(lista_similares)==49):
                return lista_similares
            if(usuario_activo.userid == usuario_comparado.userid):
                continue
            indice  = IndiceJaccard.calcularUsuarioPerfil(self,usuario_activo, usuario_comparado)
            usuario_calculado = Userid_ProfileCalculado()
            usuario_calculado.userid_profile = usuario_comparado
            usuario_calculado.indiceJ = indice
            lista_similares.append(usuario_calculado)
			
        lista_similares = sorted(lista_similares,key = Userid_ProfileCalculado.indiceJaccard, reverse = True)
        return lista_similares
    
    def indiceJ1(usuario_calculado):
        return str(usuario_calculado.indiceJ)	
    
    def calcularUsuarioPerfil(self,usuario_activo, usuario_comparado):
        tam_ua = IndiceJaccard.tamanoUsuarioPerfil(self, usuario_activo)
        tam_uc = IndiceJaccard.tamanoUsuarioPerfil(self, usuario_comparado)
        interseccion = IndiceJaccard.interseccionUsuarioPerfil(self,usuario_activo, usuario_comparado)
        indice = interseccion / (tam_ua + tam_uc - interseccion)
        return indice
        
    def tamanoUsuarioPerfil(self,usuario_perfil):
        tamano = 0
        if(usuario_perfil.gender):
            tamano = tamano +1
        if(usuario_perfil.age):
            tamano = tamano +1
        if(usuario_perfil.country):
            tamano = tamano +1
        return tamano          
        
    def interseccionUsuarioPerfil(self,usuario_activo, usuario_comparado):
        interseccion = 0
        if(usuario_activo.gender):
            if(usuario_activo.gender == usuario_comparado.gender):
                interseccion = interseccion + 1
        if(usuario_activo.age):
            if(usuario_activo.age == usuario_comparado.age):
                interseccion = interseccion + 1
        if(usuario_activo.country):
            if(usuario_activo.country == usuario_comparado.country):
                interseccion = interseccion + 1
            
        return interseccion


import pandas as pd
import numpy as np
import math

class SimilitudCoseno():
    def listaUsuariosSimilares(self,usuario_activo):
        lista_similares=[]
        
        perfiles = Userid_Profile.objects.todos();
        df_perfiles = pd.DataFrame(list(perfiles.values())) 
        
        
        genderNumber = {'m':1,'f':2}
        countryNumber = SimilitudCoseno.transforCountry(self,df_perfiles)       
        
        df_perfiles = SimilitudCoseno.procesarDatos(self,df_perfiles,genderNumber,countryNumber)    
        
        df_usuario_activo= pd.DataFrame(data=[[usuario_activo.userid, usuario_activo.gender ,usuario_activo.age,usuario_activo.country ,usuario_activo.registered ,genderNumber[usuario_activo.gender],countryNumber[usuario_activo.country] ]], columns=df_perfiles.columns)            
        
        for index, usuario_comparado in df_perfiles.iterrows():
            #print(row['c1'], row['c2'])            
            if(len(lista_similares)==49):
                return lista_similares
            if(usuario_activo.userid == usuario_comparado.userid):
                continue
            
            cosine  = SimilitudCoseno.calcularUsuarioPerfil(self,df_usuario_activo, usuario_comparado)
            usuario_calculado = Userid_ProfileCalculado()
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
        pa = int(df_usuario_activo.age)      * int(df_usuario_comparado.age)
        pc = int(df_usuario_activo.countryN) * int(df_usuario_comparado.countryN)
        
        cg_a = int(df_usuario_activo.genderN)  * int(df_usuario_activo.genderN)
        ca_a = int(df_usuario_activo.age)      * int(df_usuario_activo.age)
        cc_a = int(df_usuario_activo.countryN) * int(df_usuario_activo.countryN)
        
        m_a = math.sqrt(cg_a+ca_a+cc_a)
        
        cg_c = int(df_usuario_comparado.genderN)  * int(df_usuario_comparado.genderN)
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
        
    
    def procesarDatos(self,df_perfiles,genderNumber, countryNumber):  
        
        df_perfiles['genderN'] = [genderNumber[g] for g in df_perfiles.gender]  
        
        df_perfiles['countryN']=[countryNumber[c] for c in df_perfiles.country] 
        
        return df_perfiles
           
            
