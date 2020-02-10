from django.contrib import admin
from .models import Category, Record, Sheet
from accounts.models import Relationship

# Register your models here.
admin.site.register(Sheet)
admin.site.register(Category)
admin.site.register(Record)
admin.site.register(Relationship)