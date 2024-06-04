# models.py
from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word

class Image(models.Model):
    # word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='word_images/', null=True, blank=True)

    # def __str__(self):
    #     return self.word

class ProductDetails(models.Model):
    productId = models.CharField(max_length=20, primary_key=True)
    category = models.CharField(max_length=20)
    item = models.CharField(max_length=30)
    description = models.CharField(max_length=20)
    units = models.CharField(max_length=10)
    thresholdValue = models.IntegerField()
    image = models.JSONField()

    class Meta:
        db_table = 'productDetails'