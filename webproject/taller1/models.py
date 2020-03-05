from django.db import models
from django.db.models import Count
import random


# Create your models here.

class Userid_ProfileManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('userid'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]
    def todos(self):
        return self.all()
    

class Userid_Profile(models.Model):
    userid = models.CharField(primary_key=True, max_length=20)
    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    registered = models.CharField(max_length=100, blank=True, null=True)
    
    objects = Userid_ProfileManager()

   
    def __str__(self):
        return str(self.userid)
    
class Userid_ProfileCalculado(Userid_Profile):
    userid_profile = Userid_Profile()
    indiceJ = models.FloatField()
    cosine = models.FloatField()
    
    def indiceJaccard(self):
        return str(self.indiceJ)
    
    def similarityCosine(self):
        return str(self.cosine)

class Userid_Timestamp(models.Model):
    c_timestamp = models.CharField(max_length=30)
    codigo1 = models.CharField(max_length=50, blank=True, null=True)
    artist = models.CharField(max_length=300)
    codigo2 = models.CharField(max_length=50,blank=True, null=True)
    song = models.CharField(max_length=400)
    userid_Profile = models.ForeignKey(Userid_Profile, on_delete=models.CASCADE)
    
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
    
    class Meta:
        ordering = ["-c_timestamp"]
        
    def __str__(self):
        return str(self.id)
		
		
