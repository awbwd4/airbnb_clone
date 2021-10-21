from django.db import models

# Create your models here.
class TimeStampModel(models.Model):

    """Time Stamp Model"""

    class Meta:
        # 이 timestampModel이 데이터베이스에 등록되지 않도록 abstract로 만듦
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
