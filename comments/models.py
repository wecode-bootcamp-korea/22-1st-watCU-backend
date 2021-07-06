from django.db import models

class Comment(models.Model):
    content        = models.CharField(max_length=200)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', related_name='child_comment', on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'comments'