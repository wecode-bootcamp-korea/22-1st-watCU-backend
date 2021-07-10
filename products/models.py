from django.db import models

class Category(models.Model):
    name      = models.CharField(max_length=20)
    image_url = models.URLField()

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    korean_name     = models.CharField(max_length=20)
    english_name    = models.CharField(max_length=45, null=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    description     = models.CharField(max_length=200)
    category        = models.ForeignKey('Category', on_delete=models.CASCADE)
    # rated_users     = models.ManyToManyField('users.User', related_name='rated_products', through='ratings.Rating') 
    # liked_users     = models.ManyToManyField('users.User', related_name='liked_products', through='likes.Like')
    commented_users = models.ManyToManyField('comments.Comment', related_name='commented_products', through='comments.Comment')

    class Meta:
        db_table = 'products'

class Image(models.Model):
    image_url = models.URLField()
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'