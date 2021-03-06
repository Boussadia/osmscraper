from django.db import models

class Task(models.Model):
	key = models.CharField(max_length=32)
	hitId = models.CharField(max_length = 100, null = True)
	osm_from = models.CharField(max_length = 100)
	osm_to = models.CharField(max_length = 100)
	reference = models.CharField(max_length = 100)
	processed = models.BooleanField(default = False)

class ResultTask(models.Model):
	assignementId = models.CharField(max_length = 100)
	workerId = models.CharField(max_length = 100, null = True)
	task = models.ForeignKey(Task)
	reference = models.CharField(max_length = 100, null = True)

	class Meta:
		unique_together = ('task', 'assignementId', 'workerId')
