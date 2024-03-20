from django.contrib import admin
from .models import Purchase, AssetClass, Currency
# Register your models here.




admin.site.register(Purchase)
admin.site.register(AssetClass)
admin.site.register(Currency)
