from django.db import models

from dalliz.models import Category_sub as Category_dalliz
from dalliz.models import Category as Dalliz_category
from dalliz.models import Brand as Brand_dalliz
from dalliz.models import Unit as Unit_dalliz
from dalliz.models import Product as Dalliz_product
from tags.models import Tag

class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

class Category_sub_level_1(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_main)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Category_sub_level_2(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_1)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Category_final(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_2)
	url = models.CharField(max_length=9999)
	dalliz_category = models.ManyToManyField(Category_dalliz, related_name="monoprix_category_final_category_dalliz")

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	dalliz_brand = models.ForeignKey(Brand_dalliz, null=True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dalliz_unit = models.ManyToManyField(Unit_dalliz, related_name="monoprix_unit_dalliz_unit")

	def __unicode__(self):
		return self.name

class Product(models.Model):
	reference = models.CharField(max_length=9999, unique=True)
	title = models.CharField(max_length=1000)
	url = models.CharField(max_length=9999)
	brand = models.ForeignKey(Brand)
	price = models.FloatField(null = True)
	unit_price = models.FloatField(null = True)
	unit = models.ForeignKey(Unit)
	image_url = models.CharField(max_length=9999)
	promotion = models.CharField(max_length=9999, null = True)
	category = models.ManyToManyField(Category_final)

	description = models.TextField(null=True)
	ingredients = models.TextField(null=True)
	valeur_nutritionnelle = models.TextField(null=True)
	conservation = models.TextField(null=True)
	conseil = models.TextField(null=True)
	composition = models.TextField(null=True)

	dalliz_url = models.CharField(max_length=9999, null=True)
	dalliz_product = models.ForeignKey(Dalliz_product, null=True)


	def __unicode__(self):
		return self.title

class Product_history(models.Model):
	product = models.ForeignKey(Product)
	timestamp = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	unit_price = models.FloatField()
	promotion = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.product.title+' - '+str(self.timestamp)+' - '+str(self.price)

class Cart(models.Model):
	session_key = models.CharField(max_length=1000, unique= True)
	products = models.ManyToManyField(Product, through='Cart_content')

class Cart_content(models.Model):
	cart = models.ForeignKey(Cart)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=0)

	class Meta:
		unique_together = ("cart", "product")

class User(models.Model):
	first_name = models.CharField(max_length=1000, default='')
	last_name = models.CharField(max_length=1000, default='')
	MAN = 'M'
	WOMAN = 'W'
	UNDEF = ''
	SEX = (
		(MAN, 'Homme'),
		(WOMAN, 'Femme'),
		(UNDEF, '')
	)
	sex = models.CharField(max_length=1, choices=SEX, default=UNDEF)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=1000)
	cart = models.ForeignKey(Cart , null = True)
	created = models.DateTimeField(auto_now_add=True)
	token = models.CharField(max_length=1000, null=True)

	def __unicode__(self):
		return self.first_name+' '+self.last_name

#----------------------------------------------------------------------------------------------------
#
#										NEW MODELS FOR REFACTORING
#
#----------------------------------------------------------------------------------------------------

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

class NewBrand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_brand = models.ForeignKey('self', null=True)

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

	def __unicode__(self):
		if self.name is not None:
			return self.name
		else:
			return self.reference

class History(models.Model):
	product = models.ForeignKey(NewProduct)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField(null = True)
	unit_price = models.FloatField(null = True)
	store = models.ForeignKey(Store, null = True)
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
	store = models.ForeignKey(Store, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

	class Meta:
		unique_together = ("reference", "store")
		
