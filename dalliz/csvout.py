#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv, codecs, cStringIO
import re

from bs4 import BeautifulSoup, Comment

from auchan.models import Product as AuchanProduct
from monoprix.models import Product as MonoprixProduct
from ooshop.models import Product as OoshopProduct
from dalliz.models import Category

# from cart.dalliz.dallizcartcontroller import DallizCartController

from ooshop.models import Product as OoshopProduct
from monoprix.models import Product as MonoprixProduct
from ooshop.models import Product as OldOoshopProduct

from matcher.base.stemmer import BaseHTMLStemmer

from gensim import corpora, models, similarities

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

DALLIZ_CATEGORY_ID = 693

BASE_PATH = '/Users/ahmed/Desktop'

def extract_text(soup):
	"""
		Extracts text form beautifulsoup object.
	"""
	# Extracting comments
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	[comment.extract() for comment in comments]
	text = ''.join(soup.findAll(text=True))
	text = ' '.join(text.split())
	return text

# Auchan
def do_auchan():
	auchan_products = AuchanProduct.objects.filter(dalliz_category__parent_category__id = DALLIZ_CATEGORY_ID, html__isnull = False)
	auchan_csv_file = open(BASE_PATH+'/auchan.csv','wb')
	with auchan_csv_file as f:
		writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerows([[unicode(a.id), a.name, (lambda x : x.name if x is not None else '')(a.brand), a.url, extract_text(BeautifulSoup(a.html, "lxml", from_encoding = 'utf-8'))] for a in auchan_products])

	auchan_csv_file.close()

# Monoprix
def do_monoprix():
	monoprix_products = MonoprixProduct.objects.filter(dalliz_category__parent_category__id = DALLIZ_CATEGORY_ID, html__isnull = False)
	monoprix_csv_file = open(BASE_PATH+'/monoprix.csv','wb')
	with monoprix_csv_file as f:
		writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerows([[unicode(a.id), a.name, (lambda x : x.name if x is not None else '')(a.brand), a.url, extract_text(BeautifulSoup(a.html, "lxml", from_encoding = 'utf-8'))] for a in monoprix_products])

	monoprix_csv_file.close()

# Ooshop
def do_ooshop():
	ooshop_products = OoshopProduct.objects.filter(dalliz_category__parent_category__id = DALLIZ_CATEGORY_ID, html__isnull = False)
	ooshop_csv_file = open(BASE_PATH+'/ooshop.csv','wb')
	with ooshop_csv_file as f:
		writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerows([[unicode(a.id), a.name, (lambda x : x.name if x is not None else '')(a.brand), a.url, extract_text(BeautifulSoup(a.html, "lxml", from_encoding = 'utf-8'))] for a in ooshop_products])

	ooshop_csv_file.close()

# Tags
def do_tags():
	categories = Category.objects.filter(parent_category__id = DALLIZ_CATEGORY_ID)
	tags = []
	for c in categories:
		tags = tags + list(c.tags.all())
	tags_csv_file = open(BASE_PATH+'/tags.csv','wb')
	with tags_csv_file as f:
		writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerows([[t.name] for t in tags])

	tags_csv_file.close()

# Categories
def do_categories():
    categories = Category.objects.all()
    rows = []
    for c in categories:
        tags = c.tags.all()
        if len(tags)>0:
            row = [c.name] + list([t.name for t in tags])
            rows.append(row)

    categories_csv_file = open(BASE_PATH+'/categories.csv','wb')
    with categories_csv_file as f:
        writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def do_score_test():
    monoprix_urls = [
        'http://courses.monoprix.fr/RIDE/Cafe-moulu-pur-arabica-intense-1113676',
        'http://courses.monoprix.fr/RIDE/Cafe-moulu-pur-arabica-Bolivie-1043047',
        'http://courses.monoprix.fr/RIDE/Cafe-moulu-pur-arabica-doux-1314',
        'http://courses.monoprix.fr/RIDE/Cafe-moulu-pur-arabica-doux-1702',
        'http://courses.monoprix.fr/RIDE/Cafe-moulu-pur-arabica-Colombie-9002'
        ]
    cart = DallizCartController()
    for url in monoprix_urls:
        cart.empty()
        print url
        p = MonoprixProduct.objects.get(url = url)
        cart.add_product(p)

def get_stemmed_documents(products):
    reg = re.compile(r'\b[^\W\d]{3,}\b', re.U)
    documents = [{'id': p.id, 'text': reg.findall(unicode(BaseHTMLStemmer(p.html).extract_text().text.lower()))} for p in products]
    return documents

def buid_index(products):
    documents = get_stemmed_documents(products)
    # Generate dictionnary
    texts = [d['text'] for d in documents]
    dictionnary = corpora.Dictionary(texts)

    # Generating corpus
    corpus = [dictionnary.doc2bow(text) for text in texts]
    # Now converting to lda
    tfidf = models.TfidfModel(corpus, normalize=True)
    # Generating index
    # index = similarities.MatrixSimilarity(tfidf[corpus])
    result = []
    for token, idtoken in dictionnary.token2id.iteritems():
        result.append( {'idtoken':idtoken, 'token': token, 'score': tfidf.idfs[idtoken]})
    return sorted(result, key=lambda item: -item['score'])[:50]

def do_50_tags():
    osms = ['auchan', 'ooshop', 'monoprix']
    categories_tags_csv_file = open(BASE_PATH+'/categories_tags.csv','wb')
    with categories_tags_csv_file as f:
        writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for c in Category.objects.all():
            print c.name
            tags = {}
            products = []
            for osm in osms:
                osm_categories = getattr(c, osm+'_category_dalliz_category').all()
                if len(osm_categories)>0:
                    for osm_category in osm_categories:
                        products = products + list(osm_category.product_set.filter(html__isnull = False))
            if len(products)>0:
                row = [c.name] + [ t['token'] for t in buid_index(products)]
                # tags.append({'name':c.name, 'tags':buid_index(products)})
                writer.writerow(row)
    return tags


def do_tags_categories():
    categories_tags_csv_file = open('categories_tags.csv','wb')
    rows = []
    for c in Category.objects.all():
        #if len(c.product_set.filter(html__isnull = False))>0:
        row = [c.name]+[t.name for t in c.tags.all()]
        rows.append(row)

    with categories_tags_csv_file as f:
        writer = UnicodeWriter(f, delimiter='\t')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)
