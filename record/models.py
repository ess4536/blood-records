from django.db import models
from datetime import datetime
from accounts.models import CustomUser

# Create your models here.
class Sheet(models.Model):
    username = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    name = models.TextField(verbose_name="シート名", blank=True, max_length=30)

    class Meta:
        verbose_name_plural = "Sheet"
    def __str__(self):
        return self.name

class Category(models.Model):
    """ カテゴリーモデル """

    username = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    sheet = models.ForeignKey('Sheet', verbose_name="シート", on_delete=models.PROTECT)
    name = models.TextField(verbose_name="カテゴリー名", blank=True, max_length=30)
    description = models.TextField(verbose_name="説明", blank=True, null=True, max_length=50)
    axis = models.TextField(verbose_name="軸変数", max_length=10, blank=True, null=True)
    upper = models.FloatField(verbose_name="上限値", blank=True, null=True)
    lower = models.FloatField(verbose_name="下限値", blank=True, null=True)
    class Meta:
        verbose_name_plural ="Category"

    def __str__(self):
        return self.name

class Record(models.Model):
    """ レコードモデル """

    username = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name="カテゴリー", on_delete=models.PROTECT)
    value = models.FloatField(verbose_name="数値")
    date = models.DateField(verbose_name="日付", default=datetime.now)

    class Meta:
        verbose_name_plural = 'Record'