from django.db import models

from dalliz.models import Category_sub as Category_dalliz
from dalliz.models import Category as Dalliz_category
from dalliz.models import Brand as Brand_dalliz
from dalliz.models import Unit as Unit_dalliz
from dalliz.models import Product as Dalliz_product
from tags.models import Tag

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
	monoprix_product = models.ForeignKey(Product_monoprix, null=True, related_name="ooshop_monoprix_product")
	dalliz_product = models.ForeignKey(Dalliz_product, null=True, related_name="ooshop_product_dalliz_product")

	def __unicode__(self):
		if self.title is not None:
			return self.title
		else:
			return self.reference

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


#----------------------------------------------------------------------------------------------------
#
#										NEW MODELS FOR REFACTORING
#
#----------------------------------------------------------------------------------------------------

class ShippingArea(models.Model):
	city_name = models.TextField(null=True)
	postal_code = models.TextField(null=True)
	is_shipping_area = models.BooleanField(default=False)

	def __unicode__(self):
		if self.city_name is not None and self.postal_code is not None:
			return "%s (%s)"%(self.city_name, self.postal_code)
		else:
			return "Default Shipping Area"

class Category(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey('self', null = True)
	url = models.CharField(max_length=9999, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	exists = models.BooleanField(default = True)

	# Dalliz category association
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="ooshop_category_dalliz_category")

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class NewBrand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	image_url = models.CharField(max_length=9999, null = True)
	parent_brand = models.ForeignKey('self', null = True)

	def __unicode__(self):
		return self.name


class NewProduct(models.Model):
	reference = models.CharField(max_length=9999, null=True, unique = True) # Is not pk because of multi promotion
	name = models.CharField(max_length=1000, null = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	url = models.CharField(max_length=9999, null = True)
	brand = models.ForeignKey(NewBrand, null = True)
	unit = models.ForeignKey(Unit, null = True)
	image_url = models.CharField(max_length=9999, null = True)
	categories = models.ManyToManyField(Category, null = True)
	goodie = models.BooleanField(default=False)
	exists = models.BooleanField(default=True)

	# Product detailed description
	origine = models.TextField(null=True)
	informations = models.TextField(null=True)
	ingredients = models.TextField(null=True)
	conservation = models.TextField(null=True)
	conseils = models.TextField(null=True)
	composition = models.TextField(null=True)
	avertissements = models.TextField(null=True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 
	stemmed_text = models.TextField(max_length=9999999999999999999999, null = True) # stemmed text of product 

	# Content of product
	package_quantity = models.IntegerField(null=True)
	package_measure = models.FloatField(null=True)
	package_unit = models.TextField(null=True)

	# Final tags and dalliz_categories
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="ooshop_product_dalliz_category")
	tag = models.ManyToManyField(Tag, related_name="ooshop_product_tag_dalliz_tag")

	def __unicode__(self):
		if self.name is not None:
			return self.name
		else:
			return self.reference

class History(models.Model):
	product = models.ForeignKey(NewProduct)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	unit_price = models.FloatField()
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

class Promotion(models.Model):
	SIMPLE = 's'
	MULTI = 'm'
	TYPES = (
		(SIMPLE, 'simple'),
		(MULTI, 'multi')
	)
	reference = models.CharField(max_length=9999, null=True)
	url = models.CharField(max_length=9999, null = True)
	type = models.CharField(max_length=1, choices=TYPES, default=SIMPLE)
	image_url = models.CharField(max_length=9999, null = True)
	content = models.ManyToManyField(NewProduct)
	before = models.FloatField() # Price before any promotion
	after = models.FloatField() # Price during promotion
	unit_price = models.FloatField(null=True)
	start = models.DateField(null = True)
	end = models.DateField(null = True)
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product

	class Meta:
		unique_together = ("reference", "shipping_area") 


