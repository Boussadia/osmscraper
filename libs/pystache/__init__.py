from libs.pystache.template import Template
from libs.pystache.view import View
from libs.pystache.loader import Loader

def render(template, context=None, **kwargs):
    context = context and context.copy() or {}
    context.update(kwargs)
    return Template(template, context).render()
