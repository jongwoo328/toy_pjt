from django.db import models

# Create your models here.
class Hotdeal(models.Model):
    key = models.CharField(max_length=100),
    target = models.IntegerField(choices=((1, "제목"), (2, "내용"), (3, "제목 + 내용")), default=1)
