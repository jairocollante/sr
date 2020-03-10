from django.db import models
from django.db.models import Count
import random
from django.core.validators import MaxValueValidator, MinValueValidator


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
    gender = models.CharField(max_length=1, blank=True, null=True, choices= ([('m','Masculino'),('f','Femenino')]))
    age = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(14), MaxValueValidator(70)])
    country = models.CharField(max_length=100, blank=True, null=True)
    registered = models.CharField(max_length=100, blank=True, null=True)
    
    objects = Userid_ProfileManager()

   
    def __str__(self):
        return str(self.userid)
    
class Userid_ProfileCalculado(Userid_Profile):
    userid_profile = Userid_Profile()
    indiceJ = models.FloatField()
    cosine = models.FloatField()
    pearson = models.FloatField()
    class Meta:
        managed = False

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
		
class Userid_Rating(models.Model):    
    art_id = models.IntegerField(null=False)
    count = models.IntegerField(null=False)
    rating = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
   
    def __str__(self):
        return str(self.user_id + "-" + self.art_id)
		
class Userid_NUserId(models.Model):
    userid = models.CharField(max_length=20)
    n_userid = models.IntegerField(null=True)
   
    def __str__(self):
        return str(self.userid)
		
    def incrementNumber(self):
        last_n = Userid_NUserId.objects.all().order_by('userid').last()
        print("last_n=",last_n)
        if not last_n:
            return 0
        else:
            return last_n.n_userid + 1

class Artist_NArtist(models.Model):
    artist = models.CharField(max_length=300)
    n_artist = models.IntegerField(null=True)
   
    def __str__(self):
        return str(self.artist)

class Pred_Coseno_II(models.Model):
    user_id = models.IntegerField(null = False)
    art_id = models.IntegerField(null = False)
    r_ui = models.IntegerField(null = True)
    est = models.IntegerField(null = False)
    details = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user_id + "-" + self.art_id)

class Pred_Pearson_ii(models.Model):
    user_id = models.IntegerField(null = False)
    art_id = models.IntegerField(null = False)
    r_ui = models.FloatField(null = True)
    est = models.FloatField(null = False)
    details = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user_id + "-" + self.art_id)
