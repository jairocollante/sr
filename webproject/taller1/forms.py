from django import forms
from django.forms import ModelForm


from taller1.models import Userid_Profile, Userid_Timestamp

class T1LoginForm(forms.Form):
    userid = forms.CharField(label='Usuario:',max_length=20)
    pws = forms.CharField(label='Contraseña:',max_length=20, required=False)
    
    def doLogin(self):
        print("Hacer login")
        userid = self.data['userid']
        print("userid",userid)
        usuario = Userid_Profile.objects.filter(userid=userid)
        print("encontrado",usuario)        
        return usuario

class Userid_ProfileForm(ModelForm):
    class Meta:
        model = Userid_Profile
        fields = '__all__'
		

class Userid_TimestampForm(ModelForm):
    class Meta:
        model = Userid_Timestamp
        fields = '__all__'
