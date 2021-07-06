from django.db import models

class Like(models.Model):
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'