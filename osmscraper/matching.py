#!/usr/bin/python
# -*- coding: utf-8 -*-

from osm_matcher import *
from django.core.mail import send_mail

def perform_monoprix_telemarket_matching():
	import time
	t0 = time.time()
	monoprix = Monoprix_matcher()
	telemarket = Telemarket_matcher()
	monoprix.start_process(telemarket.products())
	print time.time() - t0

def perform_ooshop_brand_matching():
	import time
	t0 = time.time()
	dalliz = Dalliz_brand_matcher()
	ooshop = Ooshop_brand_matcher()
	dalliz.start_process(ooshop.brands())
	print time.time() - t0

def perform_ooshop_monoprix_matching():
	import time
	t0 = time.time()
	monoprix = Monoprix_matcher()
	monoprix.set_sql_query(("SELECT monoprix_product.id, (unaccent(lower(title))) as content, monoprix_unit_dalliz_unit.to_unit_id as unit, monoprix_brand.dalliz_brand_id as dalliz_brand "
				"FROM monoprix_product "
				"JOIN monoprix_unit_dalliz_unit ON monoprix_product.unit_id = monoprix_unit_dalliz_unit.from_unit_id "
				"JOIN monoprix_brand on monoprix_brand.id = monoprix_product.brand_id "
				"ORDER BY length(title) DESC"))
	ooshop = Ooshop_matcher()
	monoprix.start_process(ooshop.products(), brand = True, osm = 'ooshop')
	print time.time() - t0