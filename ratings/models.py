from django.db import models

class Rating(models.Model):
    rating  = models.DecimalField(max_digits=2, decimal_places=1)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ratings'