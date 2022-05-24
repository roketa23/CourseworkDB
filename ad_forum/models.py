import datetime
from django.db import models


class Director(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(default='1967-06-01')
    photo = models.ImageField()
    bio = models.CharField(max_length=255)


class Post(models.Model):
    name = models.CharField(max_length=50)
    mark = models.IntegerField()
    rating = models.FloatField()
    type = models.CharField(max_length=50)
    poster = models.ImageField()
    date_of_public = models.DateField(default=datetime.date.today())
    address = models.CharField(max_length=50)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)


class Review(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today())
    likes_count = models.IntegerField()
    dislikes_count = models.IntegerField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
