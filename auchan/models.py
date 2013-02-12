from django.db import models

# Create your models here.

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
	url = models.CharField(max_length=9999, null=True, unique = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)

# 	class Meta:
# 		unique_together = ("name", "parent_category")

# 	def __unicode__(self):
# 		return self.name

# class Brand(models.Model):
# 	name = models.CharField(max_length=100, unique=True)
# 	image_url = models.CharField(max_length=9999, null = True)

# 	def __unicode__(self):
# 		return self.name


# class Product(models.Model):
# 	reference = models.CharField(max_length=9999, null=True, unique = True) # Is not pk because of multi promotion
# 	name = models.CharField(max_length=1000, null = True)
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
# 	url = models.CharField(max_length=9999, null = True)
# 	brand = models.ForeignKey(NewBrand, null = True)
# 	unit = models.ForeignKey(Unit, null = True)
# 	image_url = models.CharField(max_length=9999, null = True)
# 	categories = models.ManyToManyField(Category, null = True)
# 	goodie = models.BooleanField(default=False)
# 	exists = models.BooleanField(default=True)

# 	# Product detailed description
# 	origine = models.TextField(null=True)
# 	informations = models.TextField(null=True)
# 	ingredients = models.TextField(null=True)
# 	conservation = models.TextField(null=True)
# 	conseils = models.TextField(null=True)
# 	composition = models.TextField(null=True)
# 	avertissements = models.TextField(null=True)
# 	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

# 	# Content of product
# 	package_quantity = models.IntegerField(null=True)
# 	package_measure = models.FloatField(null=True)
# 	package_unit = models.TextField(null=True)

# 	def __unicode__(self):
# 		if self.name is not None:
# 			return self.name
# 		else:
# 			return self.reference

# class History(models.Model):
# 	product = models.ForeignKey(NewProduct)
# 	created = models.DateTimeField(auto_now_add=True)
# 	price = models.FloatField()
# 	unit_price = models.FloatField()
# 	shipping_area = models.ForeignKey(ShippingArea, null = True)
# 	availability = models.BooleanField(default = True)
# 	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

# class Promotion(models.Model):
# 	SIMPLE = 's'
# 	MULTI = 'm'
# 	TYPES = (
# 		(SIMPLE, 'simple'),
# 		(MULTI, 'multi')
# 	)
# 	reference = models.CharField(max_length=9999, null=True, unique = True)
# 	url = models.CharField(max_length=9999, null = True)
# 	type = models.CharField(max_length=1, choices=TYPES, default=SIMPLE)
# 	image_url = models.CharField(max_length=9999, null = True)
# 	content = models.ManyToManyField(NewProduct)
# 	before = models.FloatField() # Price before any promotion
# 	after = models.FloatField() # Price during promotion
# 	unit_price = models.FloatField(null=True)
# 	start = models.DateField(null = True)
# 	end = models.DateField(null = True)
# 	shipping_area = models.ForeignKey(ShippingArea, null = True)
# 	availability = models.BooleanField(default = True)
# 	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 