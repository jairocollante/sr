from django import forms
from django.forms import ModelForm

from taller3.models import User

class T3LoginForm(forms.Form):
    userid = forms.CharField(label='Usuario:', max_length=30)
    pws = forms.CharField(label='Contraseña:', max_length=20, required=False)
    
    def doLogin(self):
        print("Hacer login")
        userid = self.data['userid']
        print("userid", userid)
        usuario = User.objects.using('db_t3').filter(user_id=userid)
        print("encontrado", usuario)        
        return usuario

class T3UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    
    
    def clean_user_id(self):
        id = self.cleaned_data['user_id']        
        usuario = User.objects.using('db_t3').filter(user_id=id)
        
        if usuario:
            raise forms.ValidationError("Usuario ya existe!")
        
        return id
    
class T3SearchForm(forms.Form):
    text = forms.CharField(label='Pelicula a calificar:', required=True, min_length=4,  max_length=20, help_text='Escriba el titulo o parte del mismo')       
    
class T3RatingForm(forms.Form):
    id = forms.CharField()   
    title = forms.CharField() 
    rating = forms.IntegerField(min_value=1, max_value=5)          
    