from django.db import models

from dalliz.models import Category as Dalliz_category
from dalliz.models import Unit as Unit_dalliz
from tags.models import Tag

class Store(models.Model):
	name = models.TextField(null=True)
	city_name = models.TextField(null=True)
	postal_code = models.TextField(null=True)
	latitude = models.FloatField(null = True)
	longitude = models.FloatField(null = True)
	fax = models.TextField(null=True)
	phone = models.TextField(null=True)
	address = models.TextField(null=True)
	chain = models.TextField(null=True)
	infos = models.TextField(null=True)
	icon = models.IntegerField(null=True)
	ctm = models.IntegerField(null=True)

	is_LAD = models.BooleanField(default = False) # LAD = Livraison a domicile

	class Meta:
		unique_together = ("name", "city_name", "postal_code", "address")

	def __unicode__(self):
		return ' %s (%s) %s %s %s '%(self.name, self.chain, self.address, self.city_name, self.postal_code)


class Category(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey('self', null = True)
	url = models.CharField(max_length=9999, null=True, unique = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	exists = models.BooleanField(default = True)

	# Dalliz category association
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="monoprix_category_dalliz_category")

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dalliz_unit = models.ManyToManyField(Unit_dalliz, related_name="monoprix_unit_dalliz_unit")

	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_brand = models.ForeignKey('self', null=True)

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
	exists = models.BooleanField(default=True)

	# Product detailed description
	description = models.TextField(null=True)
	ingredients = models.TextField(null=True)
	valeur_nutritionnelle = models.TextField(null=True)
	conservation = models.TextField(null=True)
	conseil = models.TextField(null=True)
	composition = models.TextField(null=True)
	
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 
	stemmed_text = models.TextField(max_length=9999999999999999999999, null = True) # stemmed text from product html 

	# Content of product
	package_quantity = models.IntegerField(null=True)
	package_measure = models.FloatField(null=True)
	package_unit = models.TextField(null=True)

	# Final tags and dalliz_categories
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="monoprix_product_dalliz_category")
	tag = models.ManyToManyField(Tag, related_name="monoprix_product_tag_dalliz_tag")

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
	price = models.FloatField(null = True)
	unit_price = models.FloatField(null = True)
	store = models.ForeignKey(Store, null = True)
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
	store = models.ForeignKey(Store, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

	class Meta:
		unique_together = ("reference", "store")
		ordering = ['-end']

class Cart(models.Model):
	osm = models.CharField(max_length=9999, default = 'monoprix')
	products = models.ManyToManyField(Product, through='Cart_content')

class Cart_content(models.Model):
	cart = models.ForeignKey(Cart)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=0)

	class Meta:
		unique_together = ("cart", "product")

class Cart_history(models.Model):
	cart = models.ForeignKey(Cart)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField(default = 0)
	computed = models.BooleanField(default = False)

	class Meta:
		ordering = ['cart', '-created']

