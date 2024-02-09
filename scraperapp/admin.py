from django.contrib import admin
from .models import Product,AliexpressAction,DeraahAction

# Register your models here.
admin.site.register(Product)
admin.site.register(AliexpressAction)
admin.site.register(DeraahAction)