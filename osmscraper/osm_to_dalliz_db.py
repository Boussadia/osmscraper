#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django.db import connection, transaction

from dalliz.models import Brand as Brand_dalliz
from monoprix.models import Brand as Brand_monoprix
from telemarket.models import Product as Product_telemarket

# Dictionnary of ill formated string form som brands : dirty string(key), clean string (value)
STRICT_MATCHING = {
	"{": "e",
	"nnn": "nn",
}

COMMON_STRINGS = {
	"friskies": "purina",
}
CLEAN_STINGS_MONOPRIX = COMMON_STRINGS

CLEAN_STINGS_MONOPRIX.update({
	"coca-cola":"coca cola",
	"la vielle ferme": "la vieille ferme",
	"la veille ferme": "la vieille ferme",
	"intensif peaux seches": "mixa",
	"gilette": "gillette",
	"dauvergne & ranvier": "dauvergne ranvier",
	"ballantines finest": "ballantine's",
	"thirry schweitzer": "thierry schweitzer",
	"n.a!": "n.a !",
	"bel": "apericube",
	"taft":"schwarzkopf",
	"curly": "vico",
	"ultra": "always",
	"rigoni": "rigoni di asiago",
	"tahiti": "palmolive",
	"balsen": "bahlsen",
	"crunch": "nestle",
	"neslte": "nestle",
	"mccain": "mc cain",
	"kit kat": "nestle",
	"twining": "twinings",
	"gervita": "danone",
	"dash 2en1": "dash 2 en 1",
	"mc vities": "mc vitie's",
	"mc vitties": "mc vitie's",
	"patriarche": "patriarche pere & fils",
	"bugles 3 d's": "benenuts",
	"dames de nuys": "dame de nuys",
	"head&shoulders": "head & shoulders",
	"perfect mousse": "schwarzkopf",
	"weightwatchers": "weight watchers",
	"thierry germain": "thierry germain",
	"tradition d'asie":"traditions d'asie",
	"montagnes noires": "montagne noire",
	"nicolas feuillate": "nicolas feuillatte",
	"knorr les moments gourmets": "knorr",
	"lekue gourmet": "lekue",
	"purina gourmet": "purina",
	"fructis": "garnier",
	"jardin d'orante": "le jardin d'orante",
	"les jardins d'orante": "le jardin d'orante",
	"dr.oetker": "dr oetker",
	"aquafresh3": "aquafresh",
})

CLEAN_STINGS_TELEMARKET = CLEAN_STINGS_MONOPRIX


def clean_string(str, dict_cleans):
	new_str = str

	for dirty_char, clean_char in STRICT_MATCHING.iteritems():
		new_str = clean_char.join(new_str.split(dirty_char))

	for dirty_char, clean_char in dict_cleans.iteritems():
		reg = r'( [\W]*'+re.escape(dirty_char)+'[\W]* )|( [\W]*'+re.escape(dirty_char)+'[\W]*$)|(^[\W]*'+re.escape(dirty_char)+'[\W]* )|(^[\W]*'+re.escape(dirty_char)+'[\W]*$)'
		if(len(re.findall(reg, str))>0):
			new_str = clean_char
		# print str+' -> '+new_str
	return new_str

def dictfetchall(cursor):
	"Returns all rows from a cursor as a dict"
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]

def make_matching(osm_brands, dalliz_brands, clean_strings = {}):
	matching = []

	# Generating regular expressions
	print "Compiling brand names"
	for j in xrange(0, len(dalliz_brands)):
		dalliz_brand = dalliz_brands[j]
		reg = r'( [\W]*'+re.escape(dalliz_brand['name'])+'[\W]* )|( [\W]*'+re.escape(dalliz_brand['name'])+'[\W]*$)|(^[\W]*'+re.escape(dalliz_brand['name'])+'[\W]* )|(^[\W]*'+re.escape(dalliz_brand['name'])+'[\W]*$)'
		dalliz_brand["regexp"] = re.compile(reg)

	
	for i in xrange(0, len(osm_brands)):
		osm_brand = osm_brands[i]
		brand_name = clean_string(osm_brand['name'], clean_strings)
		# print brand_name
		for j in xrange(0, len(dalliz_brands)):
			dalliz_brand = dalliz_brands[j]
			matches = []
			reg = dalliz_brand['regexp']
			if len(reg.findall(brand_name)) > 0:
				matching.append({'osm_id':osm_brand['id'], 'dalliz_id':dalliz_brand['id']})
				# print "Matching : "+osm_brand['name']+" -> "+dalliz_brand['name']
				break
	
	return matching

def print_no_matching(elements, matching):
	for i in xrange(0,len(elements)):
		brand_id = elements[i]["id"]
		is_set = False
		for j in xrange(0,len(matching)):
			if matching[j]["osm_id"] == brand_id:
				is_set = True
				break

		if not is_set:
			print "No Matching : "+elements[i]["name"]

def save_links_monoprix(matching):
	for i in xrange(0,len(matching)):
		match = matching[i]
		id_brand_dalliz = match["dalliz_id"]
		id_brand_monoprix = match["osm_id"]

		brand_monoprix = Brand_monoprix.objects.get(id=id_brand_monoprix)
		brand_dalliz = Brand_dalliz.objects.get(id=id_brand_dalliz)

		brand_monoprix.dalliz_brand = brand_dalliz
		brand_monoprix.save()

		print "Saving : "+brand_monoprix.name+" -> "+brand_dalliz.name

def save_link_telemarket(matching):
	for i in xrange(0,len(matching)):
		match = matching[i]
		id_brand_dalliz = match["dalliz_id"]
		id_product_telemarket = match["osm_id"]

		product_telemarket = Product_telemarket.objects.get(id=id_product_telemarket)
		brand_dalliz = Brand_dalliz.objects.get(id=id_brand_dalliz)

		product_telemarket.dalliz_brand = brand_dalliz
		product_telemarket.save()

		print "Saving : "+product_telemarket.title+" -> "+brand_dalliz.name


		

def perform_matching():
	cursor = connection.cursor()
	cursor.execute("SELECT id, unaccent(lower(name)) as name FROM dalliz_brand ORDER BY length(name) DESC")
	dalliz_brands = dictfetchall(cursor)

	# Monoprix brands
	cursor.execute("SELECT id, unaccent(lower(name)) as name FROM monoprix_brand WHERE length(name)>1 ORDER BY length(name) DESC")
	monoprix_brands = dictfetchall(cursor)
	matching = make_matching(monoprix_brands, dalliz_brands, CLEAN_STINGS_MONOPRIX)
	print_no_matching(monoprix_brands, matching)
	save_links_monoprix(matching)

	# Telemarket product -> brands
	cursor.execute("SELECT id, unaccent(lower(title)) as name FROM telemarket_product ORDER BY length(title) DESC")
	telemarket_products = dictfetchall(cursor)
	matching = make_matching(telemarket_products, dalliz_brands, CLEAN_STINGS_TELEMARKET )
	print_no_matching(telemarket_products, matching)
	save_link_telemarket(matching)
