from django.db import models


class Product(models.Model):
	sku = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500, blank=True, null=True)
	is_active = models.BooleanField(default=True)