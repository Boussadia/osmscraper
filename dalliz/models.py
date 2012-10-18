from django.db import models


class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Category_sub(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_category = models.ForeignKey(Category_main)

	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name