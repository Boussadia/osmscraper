from django.db import models


class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Category_sub(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_category = models.ForeignKey(Category_main)
	url = models.CharField(max_length=9999, null=True)
	position = models.IntegerField(default=0)

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
	url = models.CharField(max_length=9999, unique=True)
	brand = models.ForeignKey(Brand)
	product_categories = models.ManyToManyField(Category_sub)

	def __unicode__(self):
		return self.title