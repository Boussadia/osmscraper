from django.db import models


class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Category_sub(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_category = models.ForeignKey(Category_main)

	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=10, unique=True)

	def __unicode__(self):
		return self.name

class Product(models.Model):
	title = models.CharField(max_length=1000)
	url = models.CharField(max_length=9999)
	brand = models.ForeignKey(Brand)
	unit_price = models.FloatField()
	unit = models.ForeignKey(Unit)
	product_categories = models.ManyToManyField(Category_sub)


	class Meta:
		unique_together = ("title", "url")


	def __unicode__(self):
		return self.title