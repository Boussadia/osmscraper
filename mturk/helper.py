import hashlib
import datetime

from django.conf import settings

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement

from monoprix.models import Product as MonoprixProduct
from auchan.models import Product as AuchanProduct
from ooshop.models import Product as OoshopProduct
from mturk.models import Task, ResultTask
from matcher.models import ProductSimilarity, ProductMatch

osms = ['auchan', 'monoprix', 'ooshop']

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
					qid = question_form_answer.qid
					if qid == 'flagged':
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
			results = list(ResultTask.objects.filter(task = hit, reference__isnull = False))
			# Getting associate product
			osm_from = hit.osm_from
			osm_to = hit.osm_to
			reference = hit.reference
			OsmFromProduct = globals()['%sProduct'%(osm_from.capitalize())]
			productFrom = OsmFromProduct.objects.get(reference = reference)
			kwargs = {
				osm_from+'_product': productFrom
			}
			product_match = ProductMatch.objects.filter(**kwargs)
			if len(product_match) >0:
				product_match = product_match[0]
			else:
				product_match = None

			OsmToProduct = globals()['%sProduct'%(osm_to.capitalize())]
			length = len(results)
			values = {}

			for r in results:
				value = r.reference
				if value in values:
					values[value] = values[value] + 1.0/length
				else:
					values[value] = 1.0/length

			sorted_values = sorted(values, key = lambda x : -values[x])

			if len(sorted_values)>0:
				max_value = values[sorted_values[0]]
				if max_value>=thereshold:
					print 'Thereshold !'
					process_validation = False
					reference_match = sorted_values[0]
					if reference_match == '0' or reference_match == 0:
						# No match
						if product_match is None:
							product_match = ProductMatch(**kwargs)
						setattr(product_match, osm_to+'_product', None)
						product_match.save()
						process_validation = True
					else:
						productTo = OsmToProduct.objects.filter(reference = reference_match)
						if len(productTo) > 0:
							productTo = productTo[0]
							if product_match is None:
								kwargs_bis = {
									osm_to+'_product': productTo
								}
								product_match = ProductMatch.objects.filter(**kwargs_bis)
								if len(product_match)>0:
									product_match = product_match[0]
								else:
									product_match = ProductMatch(**kwargs)
							else:
								kwargs_bis = {
									osm_to+'_product': productTo
								}
								product_match_bis = ProductMatch.objects.filter(**kwargs_bis)

								if len(product_match_bis) == 0:
									pass
								else:
									product_match_bis = product_match_bis[0]
									# Migrate product_match_bis to product_match and delete
									for o in osms:
										if o != osm_from and o != osm_to:
											o_product = getattr(product_match_bis, o+'_product')
											setattr(product_match_bis, o+'_product', None)
											product_match_bis.save()
											setattr(product_match, o+'_product', o_product)
									product_match_bis.delete()

							setattr(product_match, osm_to+'_product', productTo)
							product_match.save()
							process_validation = True
						else:
							print 'Product from Osm_to not found ... reference = % %s'%reference_match


					if process_validation:
						for r in results:
							if r.reference == max_value:
								self.mtc.approve_assignment(r.assignementId)
							else:
								self.mtc.reject_assignment(r.assignementId)

						hit.processed = True
						hit.save()
						self.mtc.disable_hit(hit.hitId)


					# Getting Product 
				else:
					# For the moment, if threshold not ok, approve everything
					[self.mtc.approve_assignment(r.assignementId) for r in results]
					hit.processed = True
					hit.save()


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
			keywords = 'images, selecting, products, matching, match, selection'
			self.save_task()

			question = ExternalQuestion('http://www.dalliz.com/mturk/key/%s'%(self.key), 1106)
			qualifications = Qualifications()
			qualifications.add(PercentAssignmentsApprovedRequirement('GreaterThanOrEqualTo', 95))
			 
			#--------------- CREATE THE HIT -------------------
			 
			a = self.mtc.create_hit(
						question=question,

						title=title,
						description=description,
						keywords=keywords,

						reward=0.01,
						max_assignments=10,

						approval_delay=datetime.timedelta(seconds=3600*24*30), # auto-approve timeout
						duration = datetime.timedelta(seconds=3600*24*30))


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
		
