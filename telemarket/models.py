from django.db import models

from dalliz.models import Category_sub as Category_dalliz
from dalliz.models import Brand as Brand_dalliz


# Create your models here.
class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)
	url = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.name

class Category_sub_1(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_main)

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Category_sub_2(models.Model):
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=1000)
	parent_category = models.ForeignKey(Category_sub_1)

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Category_sub_3(models.Model):
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=1000)
	parent_category = models.ForeignKey(Category_sub_2)

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Category_final(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_3)
	url = models.CharField(max_length=9999)
	dalliz_category = models.ManyToManyField(Category_dalliz, related_name="telemarket_category_final_category_dalliz")

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return self.name

class Promotion(models.Model):
	type = models.CharField(max_length=1000, unique = True)

	def __unicode__(self):
		return self.type


class Product(models.Model):
	title = models.CharField(max_length=1000)
	url = models.CharField(max_length=9999)
	# brand = models.ForeignKey(Brand)
	# full_text = models.TextField()
	price = models.FloatField()
	unit_price = models.FloatField()
	unit = models.ForeignKey(Unit)
	image_url = models.CharField(max_length=9999)
	promotion = models.ForeignKey(Promotion)
	category = models.ForeignKey(Category_final)
	dalliz_brand = models.ForeignKey(Brand_dalliz, null=True)

	class Meta:
		unique_together = ("title", "url", "category")

	def __unicode__(self):
		return self.title