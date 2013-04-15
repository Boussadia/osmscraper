from django.conf import settings

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion

mtc = MTurkConnection(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
						aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
						host=settings.HOST)

title = 'Test External Hit'
description = ('Select the most appropriate answer')
keywords = 'website, rating, opinions'

question = ExternalQuestion('www.dalliz.com/mturk/test', 100)
print question.get_as_xml()
 
#--------------- CREATE THE HIT -------------------
 
mtc.create_hit(questions=question,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)
