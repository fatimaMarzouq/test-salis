from django.db import models

class Flower(models.Model):
    class Meta:
        app_label = 'testapp'
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

class OdooModel(models.Model):
    name = models.CharField(max_length=100)