from django.db import models

# Create your models here.
class Hotdeal(models.Model):
    key = models.CharField(max_length=100)
    target = models.CharField(choices=(("title", "제목"), ("content", "내용"), ("title_content", "제목 + 내용")), default="title", max_length=100)
