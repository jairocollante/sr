from django import forms
from django.forms import ModelForm

class T2LoginForm(forms.Form):
    userid = forms.CharField(label='Usuario:',max_length=20)
    pws = forms.CharField(label='Contraseña:',max_length=20, required=False)
    
    def doLogin(self):
        print("Hacer login")
        userid = self.data['userid']
        print("userid",userid)
#        usuario = Userid_Profile.objects.filter(userid=userid)
 #       print("encontrado",usuario)        
#        return usuario
        return userid
