from django.contrib import admin
from products.models import Product, Category, Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)