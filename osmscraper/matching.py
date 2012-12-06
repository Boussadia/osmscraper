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