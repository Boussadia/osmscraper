#!/usr/bin/python
# -*- coding: utf-8 -*-
from osm_matcher import *


# import time
# t0 = time.time()
# dalliz = Dalliz_matcher()
# telemarket = Telemarket_matcher()
# dalliz.start_process(telemarket.products())
# print time.time() - t0
# dalliz.save_brands_telemarket()


import time
t0 = time.time()
monoprix = Monoprix_matcher()
telemarket = Telemarket_matcher()
monoprix.start_process(telemarket.products())
print time.time() - t0