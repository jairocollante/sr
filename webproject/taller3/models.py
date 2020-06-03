from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=30)
