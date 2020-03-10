import pandas as  pd
import sqlalchemy

class SimilitudCosenoII():
  predictions = None
  def __init__(self):
    # Se cargan las predicciones
    engine = sqlalchemy.create_engine('postgresql://ugrupo06:grupo06@localhost:5432/t1')
    conn = engine.connect()

    sql_command = 'SELECT user_id, art_id, r_ui, est, details FROM public.taller1_pred_coseno_ii;'

    # Load the data
    predictions = pd.read_sql(sql_command, conn)
    print (predictions.shape)
    
    conn.close()

  def get_prediction_user(self, user_id):
    user_predictions = list(filter(lambda x: x[0]==user_id, predictions))
    #Ordenamos de mayor a menor estimación de relevancia
    user_predictions.sort(key=lambda x : x.est, reverse=True)
    #retorna las 10 primeras predicciones
    return user_predictions[0:10]