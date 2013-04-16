import hashlib

from django.conf import settings

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion

from mturk.models import Task, ResultTask

from matcher.models import ProductSimilarity


class MturkHelper(object):
	"""
		This class handles task creation for amazon mechanical task service.

		Amazon MTruk is used to crowdsource matching products.

		Initialisation :
			- reference : reference of the product
			- osm_from : the origin osm of a product
			- osm_to : the osm to look into
	"""
	if settings.SANDBOX:
		AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
		AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
	else:
		AWS_SECRET_ACCESS_KEY = 'e6/8e5lcCcESPKT/fe6kYkJtf0+7F2w7459WTJ0v'
		AWS_ACCESS_KEY_ID = 'AKIAIP5JQO7FQX6Q7JAQ'


	def __init__(self, reference = None, osm_from = None, osm_to = None, key = None, hitid = None):
		self.reference = reference
		self.osm_from = osm_from
		self.osm_to = osm_to
		self.key = key
		self.hitid = hitid
		if key is None:
			self.task = None
		else:
			self.task = self.get_task()

		self.mtc = MTurkConnection(aws_access_key_id=MturkHelper.AWS_ACCESS_KEY_ID,
									aws_secret_access_key=MturkHelper.AWS_SECRET_ACCESS_KEY,
									host=settings.HOST)

	def get_all_reviewable_hits(self):
		page_size = 50
		hits = self.mtc.get_reviewable_hits(page_size=page_size)
		print "Total results to fetch %s " % hits.TotalNumResults
		print "Request hits page %i" % 1
		total_pages = float(hits.TotalNumResults)/page_size
		int_total= int(total_pages)
		if(total_pages-int_total>0):
			total_pages = int_total+1
		else:
			total_pages = int_total
		pn = 1
		while pn < total_pages:
			pn = pn + 1
			print "Request hits page %i" % pn
			temp_hits = self.mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
			hits.extend(temp_hits)

		return hits

	def get_hits(self):
		hits = self.get_all_reviewable_hits()
		
		for hit in hits:
			print "####################"
			print "--------------------"
			print "HitId = %s"%(hit.HITId)
			assignments = self.mtc.get_assignments(hit.HITId)
			# Getting task associated to hit
			task = Task.objects.filter(hitId = hit.HITId)
			if len(task)>0:
				task = task[0]
			else:
				task = None

			for assignment in assignments:
				print "AssignmentId = %s"%(assignment.AssignmentId)
				print "Answers of the worker %s" % assignment.WorkerId
				for question_form_answer in assignment.answers[0]:
					for value in question_form_answer.fields:
						print "%s" % (value)
						# Saving resultTask
						if task is not None:
							resulttask, created = ResultTask.objects.get_or_create(task = task, assignementId = assignment.AssignmentId)
							if created:
								resulttask.workerId = assignment.WorkerId
								resulttask.reference = value
								resulttask.save()
				print "--------------------"

	def validate(self):
		"""
			Validating results from hits
		"""
		thereshold = .7
		hits = Task.objects.filter(processed = False)

		for hit in hits:
			results = list(ResultTask.objects.filter(task = hit))
			lenght = len(results)
			values = {}

			for r in results:
				value = r.reference
				if value in values:
					r[values] = r[values] + 1
				else:
					r[values] = 1

			print values

	def generate_key(self):
		if self.key is None and self.osm_from is not None and self.osm_to is not None and self.reference is not None:
			key = '%s-%s-%s'%(self.osm_from, self.osm_to, self.reference)
			self.key = hashlib.md5(key).hexdigest()
			return self.key
		else:
			return None

	def save_task(self):
		self.generate_key()
		if self.key is not None:
			self.task, created = Task.objects.get_or_create(key = self.key, osm_from = self.osm_from, osm_to = self.osm_to, reference = self.reference)
			if self.hitid is not None and self.task.hitId is None:
				self.task.hitId = self.hitid
				self.task.save()
			self.osm_from = self.task.osm_from
			self.osm_to = self.task.osm_to
			self.reference = self.task.reference
			self.hitid = self.task.hitId


	def get_task(self):
		if self.key is not None:
			task = Task.objects.filter(key = self.key)
			if len(task)>0:
				self.task = task[0]
				self.osm_from = self.task.osm_from
				self.osm_to = self.task.osm_to
				self.reference = self.task.reference

	def get_product_similarities(self):
		kwargs = {
			'query_name': self.osm_from,
			'index_name': self.osm_to,
			self.osm_from+'_product__reference':self.reference,
			self.osm_from+'_product__brand__brandmatch__dalliz_brand__is_mdd':False,
			self.osm_to+'_product__productmatch__isnull': True
		}
		similarities = ProductSimilarity.objects.filter(**kwargs).order_by('-score')[:11]
		return similarities

	def dump(self):
		similarities = self.get_product_similarities()
		data = []
		for sim in similarities:
			product = getattr(sim, self.osm_to+'_product')
			history = product.history_set.all()[0]
			try:
				quantity = round(history.price/history.unit_price/.5)*.5

				if product.unit is not None:
					unit = product.unit.name
				else:
					unit = None
			except Exception, e:
				quantity = None
				unit = None
				
			data.append({
				'reference': product.reference,
				'img': product.image_url,
				'quantity':quantity,
				'unit':unit,
				})

		if sim:
			product = getattr(sim, self.osm_from+'_product')
			history = product.history_set.all()[0]
			try:
				quantity = round(history.price/history.unit_price/.5)*.5

				if product.unit is not None:
					unit = product.unit.name
				else:
					unit = None
			except Exception, e:
				quantity = None
				unit = None
			return {
				'product_img': product.image_url,
				'similarities': data,
				'product_quantity': quantity,
				'product_unit': unit
			}
		else:
			return {
				'product_img': None,
				'product_quantity': None,
				'product_unit': None,
				'similarities': [],
			}


	def save_result(self, assignment, reference_result = None, workerId = None):
		self.get_task()
		result = ResultTask(
			task = self.task,
			workerId = workerId,
			assignementId = assignment,
			reference = reference_result
			)
		result.save()

	def send_task(self):
		if self.osm_from is not None and self.osm_to is not None and self.reference is not None:
			title = 'Find the corresponding product'
			description = ('Select the most appropriate answer')
			keywords = 'images, selecting, products, matching'
			self.save_task()

			question = ExternalQuestion('http://www.dalliz.com/mturk/key/%s'%(self.key), 1106)
			 
			#--------------- CREATE THE HIT -------------------
			 
			a = self.mtc.create_hit(question=question,
			               max_assignments=10,
			               title=title,
			               description=description,
			               keywords=keywords,
			               duration = 3600*24*7,
			               reward=0.01)


class ProductMtruckHelper(MturkHelper):
	"""
		Initializing MTruk by product.
	"""

	def __init__(self, product, osm_from, osm_to):
		super(ProductMtruckHelper, self).__init__(product.reference, osm_from, osm_to)
		self.product = product

class CategoryMturkHelper(object):
	"""
		Sending tasks to mturk for all products in Category (Dalliz Category)
	"""

	def __init__(self, category, osm_from, osm_to):
		self.category = category
		self.osm_from = osm_from
		self.osm_to = osm_to
		self.set_products()

	def set_products(self):
		self.products = []
		kwargs = {
			'productmatch__isnull': True,
			'brand__brandmatch__dalliz_brand__is_mdd': False,
			'productsimilarity__isnull': False,
			'exsits': True,
			'stemmed_text__isnull': False
		}

		[[self.products.append(p) for p in c.product_set.filter(**kwargs)] for c in getattr(self.category, self.osm_from+'_category_dalliz_category').all()]

		self.products = list(set(self.products))

	def send_tasks(self):
		"""
			Sending tasks to amazon mturk.
		"""

		for p in self.products:
			print p
			helper = ProductMtruckHelper(p, self.osm_from, self.osm_to)
			helper.send_task()
		
