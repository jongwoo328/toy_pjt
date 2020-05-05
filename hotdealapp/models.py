from django.db import models

# Create your models here.
class Hotdeal(models.Model):
    key = models.CharField(max_length=100)
    target = models.IntegerField(choices=((1, "제목 + 내용"), (2, "제목")), default=1)
    cnt = models.IntegerField(default=1)

    # @property
    # def update_count(self):
    #     self.count = self.count+1
    #     return self.count
