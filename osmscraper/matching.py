#!/usr/bin/python
# -*- coding: utf-8 -*-
from osm_matcher import *
from django.core.mail import send_mail

from telemarket.models import Product as Telemarket_product

def perform_monoprix_telemarket_matching():
	import time
	t0 = time.time()
	monoprix = Monoprix_matcher()
	telemarket = Telemarket_matcher()
	monoprix.start_process(telemarket.products())
	print time.time() - t0