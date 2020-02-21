from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class CustomUser(AbstractUser):
    """ 拡張ユーザモデル """

    class Meta:
        verbose_name_plural = 'CustomUser'

    def get_followers(self):
        relations = Relationship.objects.filter(follow=self)
        return [relation.follower for relation in relations]

class Relationship(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="ユーザ", related_name="user", on_delete=models.PROTECT)
    follow = models.ForeignKey(CustomUser, verbose_name="フォロー", related_name="follow", on_delete=models.PROTECT)
    is_approval = models.BooleanField(verbose_name="承認", default=False)

    def __str__(self):
        return self.user.username