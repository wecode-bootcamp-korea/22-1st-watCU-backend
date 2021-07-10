from django.db                 import models
from django.db.models.deletion import CASCADE

class Status(models.Model):

    status_choice = (
        ('wish', 'Wish'),
        ('done', 'Done'),
    )

    status  = models.CharField(max_length=10, choices=status_choice)
    user    = models.ForeignKey('users.User', on_delete=CASCADE)
    product = models.ForeignKey('products.Product', on_delete=CASCADE) 

    class Meta:
        db_table = 'statuses' 

class Like(models.Model):

    user    = models.ForeignKey('users.User', on_delete=CASCADE)
    comment = models.ForeignKey('comments.Comment', on_delete=CASCADE) 

    class Meta:
        db_table = 'likes'