from django.db import models

class Task(models.Model):
	key = models.CharField(max_length=32)
	hitId = models.CharField(max_length = 100, null = True)
	osm_from = models.CharField(max_length = 100)
	osm_to = models.CharField(max_length = 100)
	reference = models.CharField(max_length = 100)

	class Meta:
		unique_together = ("key", "osm_from", "osm_to", "reference")

class ResultTask(models.Model):
	assignementId = models.CharField(max_length = 100)
	workerId = models.CharField(max_length = 100, null = True)
	task = models.ForeignKey(Task)
	reference = models.CharField(max_length = 100, null = True)