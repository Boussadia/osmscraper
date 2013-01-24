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
		return self.url

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

class Prospect(models.Model):
	mail = models.EmailField(unique = True)

	def __unicode__(self):
		return self.mail


# New models of category
class Category(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey('self', null = True)
	url = models.CharField(max_length=9999, null=True)
	position = models.IntegerField(default=0)

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

