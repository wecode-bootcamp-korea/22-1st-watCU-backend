from django.db import models

class User(models.Model):
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    email      = models.CharField(max_length=100)
    name       = models.CharField(max_length=20)
    password   = models.CharField(max_length=200)
    gender     = models.CharField(max_length=20, choices=gender_choice, null=True)
    birth      = models.DateField(null=True)
    signup_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'