#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import math

from django.db import connection, transaction

from dalliz.models import Brand as Brand_dalliz
from telemarket.models import Product as Product_telemarket
from matcher import Matcher


def dictfetchall(cursor):
	"Returns all rows from a cursor as a dict"
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]

import time
t0 = time.time()

cursor = connection.cursor()
cursor.execute("SELECT id, unaccent(lower(name)) as content FROM dalliz_brand ORDER BY length(name) DESC")
dalliz_brands = dictfetchall(cursor)

cursor.execute("SELECT id, unaccent(lower(title)) as content FROM telemarket_product ORDER BY length(title) DESC")
telemarket_products = dictfetchall(cursor)
t1 = time.time()
print "Print database accessed in : "+str(t1-t0)
matcher = Matcher(telemarket_products)
matcher.tokenize()
t2 = time.time()
print "Index built in : "+str(t2-t1)
# for i in xrange(0,len(dalliz_brands)):
# 	t2 = time.time()
# 	query = dalliz_brands[i]["content"]
# 	matcher.process_query(query)
# 	print "Query processed in : "+str(time.time()-t2)


# matcher.process_query('batonnet glace')
word = 'nestle naturnes pomme framboise des 6 mois 4 x 130 g'
index = matcher.get_index()
token = matcher.get_token(id=30)
matcher.print_matches(word)
print "Total time : "+str(time.time()-t0)