from django.db import models
    

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=50)
    review_count = models.IntegerField(null=True)
    yelping_since = models.CharField(max_length=30)
    useful = models.IntegerField(null=True)
    funny = models.IntegerField(null=True)
    cool = models.IntegerField(null=True)
    elite = models.CharField(max_length=100)
    friends = models.CharField(max_length=1000000)
    fans = models.CharField(max_length=4000)
    average_stars = models.FloatField()
    compliment_hot = models.IntegerField(null=True)
    compliment_more = models.IntegerField(null=True)
    compliment_profile = models.IntegerField(null=True)
    compliment_cute = models.IntegerField(null=True)
    compliment_list = models.IntegerField(null=True)
    compliment_note = models.IntegerField(null=True)
    compliment_plain = models.IntegerField(null=True)
    compliment_cool = models.IntegerField(null=True)
    compliment_funny = models.IntegerField(null=True)
    compliment_writer = models.IntegerField(null=True)
    compliment_photos = models.IntegerField(null=True)
   
    def __str__(self):
        return str(self.user_id)

class Business(models.Model):
    business_id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stars = models.FloatField()
    review_count = models.IntegerField()
    is_open = models.IntegerField()
    attributes = models.CharField(max_length=4000)
    categories = models.CharField(max_length=4000)
    hours = models.CharField(max_length=200)

    def __str__(self):
        return str(self.business_id)


class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=30)
    user_id = models.CharField(null=False, max_length=30)
#    business_id = models.CharField(null=False, max_length=30)
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    stars = models.IntegerField(null=True)
    useful = models.IntegerField(null=True)
    funny = models.IntegerField(null=True)
    cool = models.IntegerField(null=True)
    text = models.CharField(max_length=10000)
    date = models.CharField(max_length=20)

    def __str__(self):
        return str(self.review_id)
