from django.db import models

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return self.name

class Product(models.Model):
	title = models.CharField(max_length=1000)
	brand = models.ManyToManyField(Brand)
	full_text = models.TextField()
	price = models.FloatField()
	unit_price = models.FloatField()
	unit = models.ManyToManyField(Unit)
	image_url = models.CharField(max_length=9999)
	promotion = models.FloatField()

	def __unicode__(self):
		return self.title