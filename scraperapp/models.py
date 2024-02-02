# scraperapp/models.py
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    discount = models.CharField(max_length=50, blank=True, null=True)
    original_price = models.CharField(max_length=50, blank=True, null=True)
    units_sold = models.CharField(max_length=50, blank=True, null=True)
    shipping = models.CharField(max_length=50, blank=True, null=True)
    store = models.CharField(max_length=255, blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
