from django import forms
from taller1.models import Userid_Profile

class T1LoginForm(forms.Form):
    userid = forms.CharField(label='Usuario:',max_length=20, widget=forms.TextInput(
                                    attrs={'class':'form-control',
                                        'placeholder':'usuario_1',}))
    pws = forms.CharField(label='Contraseña:',max_length=20, widget=forms.TextInput(
                                    attrs={'class':'form-control'}))
    
    def doLogin(self):
        print("Hacer login")
        userid = self.data['userid']
        print("userid",userid)
        usuario = Userid_Profile.objects.filter(userid=userid)
        print("encontrado",usuario)        
        return usuario