# scraperapp/models.py
from django.db import models


class CvaleyAction(models.Model):
    url = models.CharField(max_length=400)
    products_number = models.IntegerField()
    repetition_interval = models.IntegerField()
    Category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Started')
    def __str__(self):
        return self.url

class ExtraAction(models.Model):
    url = models.CharField(max_length=400)
    products_number = models.IntegerField()
    repetition_interval = models.IntegerField()
    Category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Started')
    def __str__(self):
        return self.url
    
class NiceonesaAction(models.Model):
    url = models.CharField(max_length=400)
    products_number = models.IntegerField()
    repetition_interval = models.IntegerField()
    Category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Started')
    def __str__(self):
        return self.url

class DeraahAction(models.Model):
    url = models.CharField(max_length=400)
    products_number = models.IntegerField()
    repetition_interval = models.IntegerField()
    Category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Started')
    def __str__(self):
        return self.url

class AliexpressAction(models.Model):
    url = models.CharField(max_length=400)
    products_number = models.IntegerField()
    repetition_interval = models.IntegerField()
    Category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Not Started')
    def __str__(self):
        return self.url


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

    catygorie = models.CharField(max_length=50, blank=True, null=True)
    scraped_from = models.URLField(blank=True, null=True)
    # Add the DateTimeField for the time of adding the product
    added_at = models.DateTimeField(auto_now_add=True)
    added_from = models.CharField(max_length=50, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    first_img = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)


    def __str__(self):
        return self.title

