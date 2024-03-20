from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Purchase(models.Model):
    asset_class = models.CharField()
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    currency = models.CharField(max_length=3)
    quantity = models.FloatField()
    price = models.FloatField()
    fee = models.FloatField()
    comment = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker

    # class Meta:
    #     ordering = ['- date']

class AssetClass(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Asset classes"

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name


