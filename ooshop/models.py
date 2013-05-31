from django.db import models

from dalliz.models import Category as Dalliz_category
from dalliz.models import Unit as Unit_dalliz
from tags.models import Tag

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dalliz_unit = models.ManyToManyField(Unit_dalliz, null=True, related_name="ooshop_unit_dalliz_unit")

	def __unicode__(self):
		return self.name

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

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	image_url = models.CharField(max_length=9999, null = True)
	parent_brand = models.ForeignKey('self', null = True)

	def __unicode__(self):
		return self.name


class Product(models.Model):
	reference = models.CharField(max_length=9999, null=True, unique = True) # Is not pk because of multi promotion
	name = models.CharField(max_length=1000, null = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	url = models.CharField(max_length=9999, null = True)
	brand = models.ForeignKey(Brand, null = True)
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

	# for admins
	comment = models.TextField(default = "")
	processed = models.BooleanField(default = False)

	def __unicode__(self):
		if self.name is not None:
			return self.name
		else:
			return self.reference

class History(models.Model):
	product = models.ForeignKey(Product)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	unit_price = models.FloatField()
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product

	class Meta:
		ordering = ['product', '-created']

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
	content = models.ManyToManyField(Product)
	before = models.FloatField() # Price before any promotion
	after = models.FloatField() # Price during promotion
	unit_price = models.FloatField(null=True)
	start = models.DateTimeField(null = True)
	end = models.DateTimeField(null = True)
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product

	class Meta:
		unique_together = ("reference", "shipping_area") 

class Cart(models.Model):
	osm = models.CharField(max_length=9999, default = 'ooshop')
	products = models.ManyToManyField(Product, through='Cart_content')

class Cart_content(models.Model):
	cart = models.ForeignKey(Cart)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=0)

	is_user_added = models.BooleanField(default=True)
	is_match = models.BooleanField(default=False)
	is_suggested = models.BooleanField(default=False)
	is_user_set = models.BooleanField(default=False)

	# Related products
	related_osm = models.CharField(max_length=9999, null = True)
	monoprix_content = models.ForeignKey('monoprix.Cart_content', null = True, related_name = 'ooshop_monoprix_related_content', on_delete=models.SET_NULL)
	auchan_content = models.ForeignKey('auchan.Cart_content', null = True, related_name = 'ooshop_auchan_related_content', on_delete=models.SET_NULL)


	def __unicode__(self):
		return '%s - %d'%(unicode(self.product), self.quantity)

	class Meta:
		unique_together = ("cart", "product")

class Cart_history(models.Model):
	cart = models.ForeignKey(Cart)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField(default = 0)
	computed = models.BooleanField(default = False)

	class Meta:
		ordering = ['cart', '-created']

