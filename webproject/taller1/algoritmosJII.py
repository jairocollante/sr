import pandas as  pd
from collections import defaultdict
import sqlalchemy
from pickle import Unpickler

class IndiceJaccardII():
  usersPerItem = defaultdict(set)
  itemsPerUser = defaultdict(set)
  itemNames = {}
  
  # dic itemsPerUser key user-id , values lista artitas que escucha
  # dic usersPerItem key arti-id , values lista de usuarios que escuchan
  def conjunto_jaccard(self):
    # Se cargan los conjuntos
    pickled_file = open('jaccard_item_item.pickle', 'rb')
    u = Unpickler(pickled_file)
    itemsPerUser = u.load(); usersPerItem = u.load(); itemNames = u.load()
    pickled_file.close()

# Función para el cálculo del índice de Jaccard
  def Jaccard(self, s1, s2):
    number = len(s1.intersection(s2))
    denom =  len(s1.union(s2))
    return number/denom       

# Función ítems similares
# retorna los 10 items mas similares al item i en función a la similitud jaccard de los
# usuarios que  han escuchado el item i
  def mostSimilar_item(self, i, n):
    similares = []
    users = self.usersPerItem[i]
    for i2 in usersPerItem:
      if i2 is None:continue
      if i2==i:continue
      sim = Jaccard(users, usersPerItem[i2])
      similares.append((sim, i2))
    similares.sort(reverse = True)
    return similares[:n]

    def listaUsuariosSimilares(self, usuario_activo):
        
        cantidad = 10
        
        lista_similares=[]          
        udata = IndiceJaccardII.cargarDatosUserTimeStamp(self)     
        ratingsby = udata.groupby(['user_id','art_id','artname'])['art_id'].count().reset_index(name='count')
                        
        usersPerItem = defaultdict(set)
        itemsPerUser =defaultdict(set)
        itemNames={}
        
        for i,d in ratingsby.iterrows():
            user,item = d['user_id'], d['art_id']
            usersPerItem[item].add(user)
            itemsPerUser[user].add(item)
            itemNames[item] = d['artname']        
        
        lista_similares = IndiceJaccarII.rs_user_user_jaccard(self,usuario_activo,usersPerItem,itemsPerUser,itemNames,cantidad)
        
        return lista_similares[:cantidad]
    
    def listaItemsSimilares(self,usuario_activo):
        
        cantidad =10
        
        lista_similares=[]  
        udata = IndiceJaccardII.cargarDatosUserTimeStamp(self)     
        ratingsby = udata.groupby(['user_id','art_id','artname'])['art_id'].count().reset_index(name='count')
                        
        usersPerItem = defaultdict(set)
        itemsPerUser =defaultdict(set)
        itemNames={}
        
        for i,d in ratingsby.iterrows():
            user,item = d['user_id'], d['art_id']
            usersPerItem[item].add(user)
            itemsPerUser[user].add(item)
            itemNames[item] = d['artname']        
        
        lista_similares = IndiceJaccardII.rs_user_item_jaccard(self,usuario_activo,usersPerItem,itemsPerUser,itemNames,cantidad)
                
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
    
  # Función ítems que no ha consumido el usuario
  # retorna los Items que No ha consumido un usuario de una lista de items
  def items_no_in_usuario(self, items, items_u):
    items_ok = []
    for item in items:
      if item[1] not in items_u:
        items_ok.append(item)
    return items_ok

  # Retorna los Items que No ha consumido un usuario de una lista de items
  def items_no_in_usuario_lista(self, items, items_u):
    items_ok = []
    for item in items:
      if item not in items_u:
        items_ok.append(item)
    return items_ok

  # Dado un usuario recomenida items que no ha consumido en función de la similitud jaccard a items
  # que han consumido otros usuarios
  def rs_user_item_jaccard(self, userid, n):
    lista_items = self.itemsPerUser[userid]
    items_similares =[]
    for item in lista_items:
      items_similares = items_similares + (self.mostSimilar_item(item, n))
  
    items_similares = self.items_no_in_usuario(items_similares, lista_items)
    items_similares.sort(reverse=True)

    return items_similares[:n]  

  def items_most_similar(self, userid, n=10):
    return [itemNames[i[1]] for i in self.rs_user_item_jaccard(userid, n)]

'''        
    # retorna los 10 items mas similares al item i en funcion a la similitud jaccard de los usurios que  han escuchado el item i
    def mostSimilar_itemx(self,i,usersPerItem,n):
        similares=[]
        users =  usersPerItem[i]
        for i2 in  usersPerItem:
            if i2==i:continue
            sim = IndiceJaccardII.Jaccard(self,users,  usersPerItem[i2])
            similares.append((sim,i2))
        similares.sort(reverse=True)
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
            items_similares = items_similares + (IndiceJaccardII.mostSimilar_item(self,item,usersPerItem,n))
            items_similares = IndiceJaccardII.items_no_in_usuario(self,items_similares,lista_items)
            items_similares.sort(reverse=True)
            
        lista_resultante=[]
        for i in items_similares:
            lista_resultante.append(itemNames[i])
        
        return lista_resultante
    
    # dado un usuario recomenida items que no ha consumido en funcion de la similitud jaccard a usuarios que han consumido estos items
    def rs_user_user_jaccard(self,userid,usersPerItem,itemsPerUser,itemNames,n):     
        
        lista_items = itemsPerUser[userid]
        lista_usuarios = IndiceJaccardII.mostSimilar_usuario(self,userid,itemsPerUser,n)
        items_similares = set()
        items_similares_ =[]
        for user in lista_usuarios:
            for item in itemsPerUser[user[1]]:
                items_similares.add(item)
            items_similares_ = IndiceJaccardII.items_no_in_usuario_lista(self,items_similares,lista_items)
            if len(items_similares_) >= n:
                break
        
        lista_resultante=[]
        for i in items_similares_:
            lista_resultante.append(itemNames[i])
            
        return lista_resultante
'''