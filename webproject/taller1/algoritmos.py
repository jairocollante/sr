from taller1.models import Userid_Profile


class IndiceJaccard():
    
    def listaUsuariosSimilares(self,usuario_activo):
        lista_similares=[]
        perfiles = Userid_Profile.objects.todos();
        
        for usuario_comparado in perfiles:
            if(len(lista_similares)==10):
                return lista_similares
            indice  = IndiceJaccard.calcularUsuarioPerfil(self,usuario_activo, usuario_comparado)
            if(indice == 1):
                lista_similares.append(usuario_comparado)
                
        return lista_similares
                
    
    def calcularUsuarioPerfil(self,usuario_activo, usuario_comparado):
        longitud = 3
        interseccion = IndiceJaccard.interseccionUsuarioPerfil(self,usuario_activo, usuario_comparado)
        indice = interseccion / (longitud + longitud - interseccion)
        return indice
        
        
    def interseccionUsuarioPerfil(self,usuario_activo, usuario_comparado):
        interseccion = 0
        
        if(usuario_activo.userid == usuario_comparado.userid):
            return interseccion
        if(usuario_activo.gender == usuario_comparado.gender):
            interseccion = interseccion + 1
        if(usuario_activo.age == usuario_comparado.age):
            interseccion = interseccion + 1
        if(usuario_activo.country == usuario_comparado.country):
            interseccion = interseccion + 1
            
        return interseccion

        
            
            