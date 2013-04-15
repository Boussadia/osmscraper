from django.conf import settings

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion

mtc = MTurkConnection(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
						aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
						host=settings.HOST)

title = 'Test External Hit'
description = ('Select the most appropriate answer')
keywords = 'website, rating, opinions'

question = ExternalQuestion('http://www.dalliz.com/mturk/test', 500)
 
#--------------- CREATE THE HIT -------------------
 
mtc.create_hit(question=question,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)
