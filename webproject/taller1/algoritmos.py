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
			
        lista_similares = sorted(lista_similares,key =IndiceJaccard.indiceJ, reverse = True)
        return lista_similares
    
    def indiceJ(usuario_calculado):
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

        
            
            
