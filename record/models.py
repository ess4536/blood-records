from django.db import models
from datetime import datetime
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    """ カテゴリーモデル """

    sheet = models.ForeignKey('Sheet', verbose_name="シート", on_delete=models.PROTECT)
    name = models.TextField(verbose_name="カテゴリー名", blank=True, max_length=30)
    axis = models.TextField(verbose_name="軸変数", max_length=10)
    upper = models.FloatField(verbose_name="上限値", blank=True, null=True)
    lower = models.FloatField(verbose_name="下限値", blank=True, null=True)

    class Meta:
        verbose_name_plural ="Category"

    def __str__(self):
        return self.name

class Sheet(models.Model):
    """ シートモデル """

    name = models.TextField(verbose_name="シート名", blank=True, max_length=30)
    create_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sheet"
    
    def __str__(self):
        return self.name

class Record(models.Model):
    """ レコードモデル """

    user = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name="カテゴリー", on_delete=models.PROTECT)
    sheet = models.ForeignKey('Sheet', verbose_name="シート", on_delete=models.PROTECT)
    value = models.FloatField(verbose_name="数値")
    date = models.DateField(verbose_name="日付", default=datetime.now)

    class Meta:
        verbose_name_plural = 'Record'
