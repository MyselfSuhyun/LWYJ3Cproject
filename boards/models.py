from django.db import models

# Create your models here.

class Board(models.Model):
    location = models.CharField(max_length=10)
    real_tem = models.IntegerField()
    real_hum = models.IntegerField()
    api_tem = models.IntegerField()
    api_hum = models.IntegerField()
    error_tem = models.IntegerField()
    error_hum = models.IntegerField()
    created_at= models.DateTimeField(auto_now_add=True)
    writer = models.CharField(max_length=30)

class GisangGrid(models.Model):
    si = models.CharField(max_length=20)
    gu = models.CharField(max_length=20,default='default')
    do = models.CharField(max_length=20,default='default')
    gridx = models.IntegerField()
    gridy = models.IntegerField()