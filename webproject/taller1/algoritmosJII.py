import pandas as  pd
from collections import defaultdict
import sqlalchemy
from pickle import Unpickler

class IndiceJaccardII():
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

# Función ítems similares
# retorna los 10 items mas similares al item i en función a la similitud jaccard de los
# usuarios que  han escuchado el item i
  def mostSimilar_item(self, i, n):
    similares = []
    users = self.usersPerItem[i]
    for i2 in self.usersPerItem:
      if i2 is None:continue
      if i2 == i: continue
      sim = self.Jaccard(users, self.usersPerItem[i2])
      similares.append((sim, i2))
    similares.sort(reverse = True)
    return similares[:n]

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
    return [self.itemNames[i[1]] for i in self.rs_user_item_jaccard(userid, n)]
