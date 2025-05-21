from django.contrib import admin
from .models import Famili, Product, Composition, ProductMedia
# Register your models here.

admin.site.register(Famili)
admin.site.register(Product)
admin.site.register(Composition)
admin.site.register(ProductMedia)