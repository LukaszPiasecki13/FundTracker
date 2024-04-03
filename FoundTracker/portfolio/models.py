from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    operation_type = models.CharField(max_length=20)
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
        return self.operation_type


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


class Pocket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    assets = models.ManyToManyField('Asset', through='AssetAllocation')
    fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Asset(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    asset_class = models.CharField()
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class AssetAllocation(models.Model):
    pocket = models.ForeignKey(Pocket, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    average_price = models.DecimalField(max_digits=10, decimal_places=3)


