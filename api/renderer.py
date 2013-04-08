#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import itertools
from collections import defaultdict
from rest_framework.renderers import *
from StringIO import StringIO

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
                [ row.extend([h['created'] ,h['price']]) for h in product['history'] ]
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

class ProductRecomandationCSVRenderer(BaseRenderer):
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
                [ row.extend([h['created'] ,h['price']]) for h in product['history'] ]
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