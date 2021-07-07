from django.db  import models
from users.core import TimeStampModel

class User(TimeStampModel):
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    email      = models.EmailField()
    name       = models.CharField(max_length=20)
    password   = models.CharField(max_length=200)
    gender     = models.CharField(max_length=20, choices=gender_choice, null=True)
    birth      = models.DateField(null=True)

    class Meta:
        db_table = 'users'