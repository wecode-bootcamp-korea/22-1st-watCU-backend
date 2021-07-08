from django.db                 import models
from django.db.models.deletion import CASCADE

class Wish(models.Model):
    product     = models.ForeignKey('products.Product', on_delete=CASCADE)
    user        = models.ForeignKey('users.User', on_delete=CASCADE)

    class Meta:
        db_table = 'wish'

class Done(models.Model):
    product     = models.ForeignKey('products.Product', on_delete=CASCADE)
    user        = models.ForeignKey('users.User', on_delete=CASCADE)

    class Meta:
        db_table = 'done'

class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    comment = models.ForeignKey('comments.Comment', on_delete=CASCADE) 

    class Meta:
        
        db_table = 'likes'
