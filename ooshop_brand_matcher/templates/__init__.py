import os
import pystache

pystache.View.template_path = os.path.abspath(os.path.dirname(__file__))
pystache.View.template_encoding = 'utf-8'