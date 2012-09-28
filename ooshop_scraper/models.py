from django.db import models

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=1000)
	price = models.IntegerField()
	quantity = models.IntegerField()
	unit = models.CharField(max_length = 10)
	unit_price = models.IntegerField()
	url_image = models.CharField(max_length = 1000)
	url_product = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.title+" - "+str(self.price)
		