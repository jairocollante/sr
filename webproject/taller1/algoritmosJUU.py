import pandas as  pd
from collections import defaultdict
import sqlalchemy
from pickle import Unpickler

class IndiceJaccardUU():
  usersPerItem = defaultdict(set)
  itemsPerUser = defaultdict(set)
  itemNames = {}
  def __init__(self):
    # Se cargan los conjuntos
    pickled_file = open('jaccard_item_item.pickle', 'rb')
    u = Unpickler(pickled_file)
    self.itemsPerUser = u.load(); self.usersPerItem = u.load(); self.itemNames = u.load()
    pickled_file.close()

  # Función para el cálculo del índice de Jaccard
  def Jaccard(self, s1, s2):
    number = len(s1.intersection(s2))
    denom =  len(s1.union(s2))
    return number/denom       

  # Función usuarios similares
  # dado un usuario retorna los 10 usuarios mas similares al usuario i en funcion a la 
  # similitud jaccard de los items que estos usuarios consumieron
  def mostSimilar_usuario(self, i, n):
    similares = []
    items = self.itemsPerUser[i]
    for u2 in  self.itemsPerUser:
      if u2 is None:continue
      if u2==i:continue
      sim = self.Jaccard(items, self.itemsPerUser[u2])
      similares.append((sim, u2))

    similares.sort(key=lambda t: t[0],reverse= True)
    return similares[:n]

  # Función ítems que no ha consumido el usuario
  # retorna los Items que No ha consumido un usuario de una lista de ítems
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

  # dado un usuario recomenida items que no ha consumido en funcion de la similitud jaccard a usuarios que han consumido estos items
  def rs_user_user_jaccard(self, userid, n):
    lista_items = self.itemsPerUser[userid]
    lista_usuarios = self.mostSimilar_usuario(userid,n)
    items_similares = set()
    items_similares_ =[]
    for user in lista_usuarios:
      for item in self.itemsPerUser[user[1]]:
        items_similares.add(item)
      items_similares_ = self.items_no_in_usuario_lista(items_similares, lista_items)
      if len(items_similares_) >= n:
        break

    return items_similares_[:n]

  def items_most_similar(self, userid, n=10):
    return [self.itemNames[i] for i in self.rs_user_user_jaccard(userid, n)]
