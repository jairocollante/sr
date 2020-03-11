import numpy as np
import pandas as pd

class Coseno():
	def recomendacionUsuario(self,usuario_activo):
		print("Modelo Coseno Usuario")
		cant = 10
		df_mapreduce = Coseno.cargarDatos(self)
		print("df_mapreduce.shape",df_mapreduce.shape)
		df_pivot = df_mapreduce.pivot('userid','artist','count').fillna(0)
		print("Pivot.shape=", df_pivot.shape)
		lista_coseno_usuario = Coseno.iterarUsuario(self,df_pivot,usuario_activo)
		print("Termina calculo coseno=",len(lista_coseno_usuario))
		lista_coseno_usuario.sort(key=lambda k:k['coseno'], reverse = True)
		print("Termina ordenar lista coseno")
		usuario_mas_similar = lista_coseno_usuario[0]['usuario_similar']
		print("Usuario mas similar=",usuario_mas_similar)
		lista_recomendacion = Coseno.artistaMasEscuchadoPorUsuario(self,usuario_mas_similar,cant,df_pivot)
		resp = {"lista_coseno_usuario":lista_coseno_usuario[:cant],
		"lista_recomendacion":lista_recomendacion}
		return resp

	def cargarDatos(self):
		df_mapreduce = pd.read_csv('part-r-00000',sep='\t',names=['userid','artist','count'])
		return df_mapreduce.dropna()
		
	def iterarUsuario(self,df_pivot,usuario_activo):
		v_usuario_activo = df_pivot.loc[usuario_activo].values
		lista_coseno=[]
		for user_evaluado in df_pivot.index.tolist():
			if usuario_activo != user_evaluado:
				object = {}            
				object['usuario_similar']=user_evaluado
				v_usuario_evaluado = df_pivot.loc[user_evaluado].values        
				object['coseno']=Coseno.cos_sim(self,v_usuario_activo, v_usuario_evaluado)
				lista_coseno.append(object)
		return lista_coseno
		
	def valorCoseno(self):
		return val['coseno']
		
	def artistaMasEscuchadoPorUsuario(self,usuario_evaluado,cant,df_pivot):
		artistas_escuchados = df_pivot.loc[usuario_evaluado]    
		df_r = pd.DataFrame(artistas_escuchados)
		df_r = df_r.sort_values(by=[usuario_evaluado], ascending=False).index.tolist()
		return df_r[:cant]
		
	def cos_sim(self,a, b):
	#Takes 2 vectors a, b and returns the cosine similarity according 
	#to the definition of the dot product
		dot_product = np.dot(a, b)
		norm_a = np.linalg.norm(a)
		norm_b = np.linalg.norm(b)
		return dot_product / (norm_a * norm_b)
		
	def recomendacionItem(self,usuario_activo):		
		print("Modelo Coseno Item")	
		df_mapreduce = Coseno.cargarDatos(self)
		print("df_mapreduce.shape",df_mapreduce.shape)
		df_pivotA = df_mapreduce.pivot('userid','artist','count').fillna(0)
		print("Usuario Pivot.shape=", df_pivotA.shape)
		artista_activo = Coseno.artistaMasEscuchadoPorUsuario(self,usuario_activo,10,df_pivotA)
				
		cant = 10
		
		df_pivot = df_mapreduce.pivot('artist','userid','count').fillna(0)
		print("Artista Pivot.shape=", df_pivot.shape)
		lista_coseno_artista = Coseno.iterarArtistas(self,df_pivot,artista_activo[:1])
		print("Termina calculo coseno=",len(lista_coseno_artista))
		lista_coseno_artista.sort(key=lambda k:k['coseno'], reverse = True)
		print("Termina ordenar lista coseno")
		resp = {"lista_coseno_artista":lista_coseno_artista[:cant],
		"artista_activo":artista_activo}
		return resp
		
	def iterarArtistas(self,df_pivot_artista,artista_activo):
		v_artista_activo = df_pivot_artista.loc[artista_activo].values
		lista_coseno=[]
		for artista_evaluado in df_pivot_artista.index.tolist():
			if artista_activo != artista_evaluado:
				object = {}            
				object['artista_similar']=artista_evaluado
				v_artista_evaluado = df_pivot_artista.loc[artista_evaluado].values        
				object['coseno']=Coseno.cos_sim(self,v_artista_activo, v_artista_evaluado)
				lista_coseno.append(object)
		return lista_coseno