from django.db import models

# Create your models here.
def Hotdeal(models.Model):
    key = models.CharField(max_length=100),
    target = models.IntegerField(choices=((1, _("제목")), (2, _("내용")), (3, _("제목 + 내용"))), default=1)
