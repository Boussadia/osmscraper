#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import itertools
from collections import defaultdict
from rest_framework.renderers import *
from StringIO import StringIO

OSMS = ['ooshop', 'monoprix', 'auchan']

class ProductsCSVRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = 'text/csv'
    format = 'csv'
    level_sep = '.'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        table = []

        if 'products' in data:
            for product in data['products']:
                row = [product['brand']['name'], product['name'], product['osm_url'] ]
                for h in product['history']:
                    if h['is_promotion']:
                        row.extend(['PROMOTION', h['end'] ,h['price']])
                    else:
                        row.extend(['PRODUIT', h['created'] ,h['price']])
                        
                table.append(row)

        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            csv_writer.writerow([
            elem.encode('utf-8') if isinstance(elem, basestring) else elem
            for elem in row
            ])

        return csv_buffer.getvalue()

class ProductRecommendationCSVRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = 'text/csv'
    format = 'csv'
    level_sep = '.'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        table = self.render_table(data, media_type=None, renderer_context=None)
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            # print row
            csv_writer.writerow([
            elem.encode('utf-8') if isinstance(elem, basestring) else elem
            for elem in row
            ])
        print csv_buffer

        return csv_buffer.getvalue()

    def render_table(self, data, media_type=None, renderer_context=None):
        if data is None:
            return ''

        table = []
        print data['osm']

        if 'products' in data:
            for product in data['products']:
                row = [data['osm']['name'], (lambda b : b['name'] if b is not None and'name' in b else '' )(product['brand']), product['name'], product['osm_url'] ]
                for h in product['history']:
                    if h['is_promotion']:
                        row.extend(['PROMOTION', h['end'] ,h['price']])
                    else:
                        row.extend(['PRODUIT', h['created'] ,h['price']])
                # [ row.extend([(lambda x : x['created'] if 'created' in x else h['end'] )(h) ,h['price']]) for h in product['history'] ]
                table.append(row)
                if renderer_context is None or (renderer_context is not None and 'nested' not in renderer_context) or (renderer_context is not None and 'nested' in renderer_context and renderer_context['nested'] == True):
                    for osm in OSMS:
                        if osm in product and len(product[osm].keys())>0:
                            osm_product = product[osm]
                            osm_product['name'] = product['name']
                            data_nested = {
                                    'osm': {
                                        "name": osm, 
                                        },
                                    'products' : [product[osm]]
                                }
                            renderer = ProductRecommendationCSVRenderer()
                            rendered = renderer.render_table(data_nested, media_type, renderer_context = {'nested': False})
                            table.append(rendered[0])

        return table

class NewProductsCSVRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = 'text/csv'
    format = 'csv'
    level_sep = '.'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        table = self.render_table(data, media_type=None, renderer_context=None)
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        for row in table:
            # Assume that strings should be encoded as UTF-8
            # print row
            csv_writer.writerow([
            elem.encode('utf-8') if isinstance(elem, basestring) else elem
            for elem in row
            ])
        print csv_buffer

        return csv_buffer.getvalue()

    def render_table(self, data, media_type=None, renderer_context=None):
        if data is None:
            return ''

        table = []
        print data['osm']

        if 'products' in data:
            for product in data['products']:
                row = [data['osm']['name'], (lambda b : b['name'] if b is not None and'name' in b else '' )(product['brand']), product['name'], product['osm_url'] ]
                h = product['history'][-1]
                if h['is_promotion']:
                    row.extend([h['end'] ,h['price']])
                else:
                    row.extend([h['created'] ,h['price']])
                # [ row.extend([(lambda x : x['created'] if 'created' in x else h['end'] )(h) ,h['price']]) for h in product['history'] ]
                table.append(row)
                if renderer_context is None or (renderer_context is not None and 'nested' not in renderer_context) or (renderer_context is not None and 'nested' in renderer_context and renderer_context['nested'] == True):
                    for osm in OSMS:
                        if osm in product and len(product[osm].keys())>0:
                            osm_product = product[osm]
                            osm_product['name'] = product['name']
                            data_nested = {
                                    'osm': {
                                        "name": osm, 
                                        },
                                    'products' : [product[osm]]
                                }
                            renderer = ProductRecommendationCSVRenderer()
                            rendered = renderer.render_table(data_nested, media_type, renderer_context = {'nested': False})
                            table.append(rendered[0])

        return table

