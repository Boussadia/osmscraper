from django.db import models

from dalliz.models import Category_sub as Category_dalliz
from dalliz.models import Brand as Brand_dalliz
from dalliz.models import Unit as Unit_dalliz
from dalliz.models import Product as Dalliz_product

from monoprix.models import Product as Product_monoprix

class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

class Category_sub_level_1(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_main)
	url = models.CharField(max_length=9999)
	cookie = models.CharField(max_length=10000, null = True)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Category_sub_level_2(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_1)
	url = models.CharField(max_length=9999)
	cookie = models.CharField(max_length=10000, null = True)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")


class Category_final(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_2)
	url = models.CharField(max_length=9999)
	cookie = models.CharField(max_length=10000, null = True)
	dalliz_category = models.ManyToManyField(Category_dalliz, related_name="ooshop_category_final_category_dalliz")

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	dalliz_brand = models.ForeignKey(Brand_dalliz, null=True, related_name="ooshop_brand_dalliz_brand")
	dalliz_brand_m2m = models.ManyToManyField(Brand_dalliz, related_name="ooshop_brand_dalliz_brand_M2M")

	def __unicode__(self):
		return self.name

class Brand_matching(models.Model):
	score = models.FloatField()
	dalliz_brand = models.ForeignKey(Brand_dalliz)
	ooshop_brand = models.ForeignKey(Brand)

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dalliz_unit = models.ManyToManyField(Unit_dalliz, null=True, related_name="ooshop_unit_dalliz_unit")

	def __unicode__(self):
		return self.name

class Product(models.Model):
	reference = models.CharField(max_length=9999, primary_key=True)
	title = models.CharField(max_length=1000, null = True)
	url = models.CharField(max_length=9999, null = True)
	brand = models.ForeignKey(Brand, null = True)
	unit = models.ForeignKey(Unit, null = True)
	image_url = models.CharField(max_length=9999, null = True)
	category = models.ManyToManyField(Category_final, null = True)
	dalliz_product = models.ForeignKey(Dalliz_product, null=True, related_name="ooshop_product_dalliz_product")

	def __unicode__(self):
		return self.title

class Product_history(models.Model):
	product = models.ForeignKey(Product)
	timestamp = models.DateTimeField(auto_now_add=True)
	price = models.FloatField() # Price before any promotion
	unit_price = models.FloatField()
	promotion_type = models.CharField(max_length=9999)
	promotion = models.FloatField(default = 0)
	references = models.ManyToManyField(Product, related_name="ooshop_promotion_lot")


	def __unicode__(self):
		return self.product.title+' - '+str(self.timestamp)+' - '+str(self.price)

class Monoprix_matching(models.Model):
	ooshop_product = models.ForeignKey(Product)
	monoprix_product = models.ForeignKey(Product_monoprix, related_name='matching_monoprix_ooshop')
	score = models.FloatField()