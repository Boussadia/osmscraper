#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import connection


def dictfetchall(cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]
