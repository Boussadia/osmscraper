from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	stemmed_name = models.CharField(max_length=100, null = True)
	is_super_tag = models.BooleanField(default = False)

	class Meta:
		unique_together = ('name', 'is_super_tag')

	def __unicode__(self):
		return self.name
