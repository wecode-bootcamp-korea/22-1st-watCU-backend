from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=100)
    name     = models.CharField(max_length=20)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'