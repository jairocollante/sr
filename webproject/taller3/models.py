from django.db import models

# Create your models here.
class User(models.Model):
    #user_id = models.IntegerField(primary_key=True, max_length=30)
    user_id = models.PositiveIntegerField(primary_key=True)
