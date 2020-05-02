from django import forms
from django.forms import ModelForm

from taller2.models import User

class T2LoginForm(forms.Form):
    userid = forms.CharField(label='Usuario:', max_length=30)
    pws = forms.CharField(label='Contraseña:', max_length=20, required=False)
    
    def doLogin(self):
        print("Hacer login")
        userid = self.data['userid']
        print("userid", userid)
        usuario = User.objects.filter(user_id=userid)
        print("encontrado", usuario)        
        return usuario
