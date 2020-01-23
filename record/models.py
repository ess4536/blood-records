from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    """ カテゴリーモデル """

    sheet = models.ForeignKey('Sheet', verbose_name="シートID", on_delete=models.PROTECT)
    category_name = models.TextField(verbose_name="カテゴリー名", blank=True, max_length=30)
    axis = models.TextField(verbose_name="軸変数", max_length=10)
    upper = models.FloatField(verbose_name="上限値", null=True)
    lower = models.FloatField(verbose_name="下限値", null=True)

    class Meta:
        verbose_name_plural ="Category"

    def __str__(self):
        return self.category_name

class Sheet(models.Model):
    """ シートモデル """

    sheet_name = models.TextField(verbose_name="シート名", blank=True, max_length=30)
    create_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sheet"
    
    def __str__(self):
        return self.sheet_name

class Record(models.Model):
    """ レコードモデル """

    user = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name="カテゴリーID", on_delete=models.PROTECT)
    sheet = models.ForeignKey('Sheet', verbose_name="シートID", on_delete=models.PROTECT)
    value = models.FloatField(verbose_name="値")
    create_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Record'
