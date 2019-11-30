from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class comment_tbl(models.Model):
    comment = models.CharField(max_length=1000)
    rating = models.CharField(max_length=5)
    movie_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=30)
    commented_dat = models.CharField(max_length=50)

    def _str_(self):
        return self.comment