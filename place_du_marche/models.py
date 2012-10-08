from django.db import models

class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Category_sub(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_category = models.ForeignKey(Category_main)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

class Category_final(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

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
	url = models.CharField(max_length=9999, unique = True)
	brand = models.ForeignKey(Brand)
	full_text = models.TextField()
	price = models.FloatField()
	unit_price = models.FloatField()
	unit = models.ForeignKey(Unit)
	image_url = models.CharField(max_length=9999)
	promotion = models.FloatField()
	category = models.ForeignKey(Category_final)

	def __unicode__(self):
		return self.title