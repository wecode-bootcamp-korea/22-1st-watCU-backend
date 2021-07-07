from django.db  import models
from users.core import TimeStampModel

class Comment(TimeStampModel):
    content        = models.CharField(max_length=200)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', related_name='child_comment', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'comments' 