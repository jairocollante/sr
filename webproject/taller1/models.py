from django.db import models

# Create your models here.

class Userid_Profile(models.Model):
    userid = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    registered = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)
    
class Userid_Timestamp(models.Model):
    c_timestamp = models.CharField(max_length=30)
    codigo1 = models.CharField(max_length=50, blank=True, null=True)
    artist = models.CharField(max_length=300)
    codigo2 = models.CharField(max_length=50,blank=True, null=True)
    song = models.CharField(max_length=400)
    userid_Profile = models.ForeignKey(Userid_Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)