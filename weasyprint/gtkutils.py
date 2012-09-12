# coding: utf8
"""
    weasyprint.gtkutils
    -------------------

    Utilities for better Gtk Printing

    :copyright: Copyright 2011-2012 Simon Sapin and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

import cairo

from .draw import draw_page


class GtkPrint(object):
    def __init__(self, html, operation):
        self.html = html
        self.operation = operation
        self.operation.connect('begin-print', self._on__begin_print)
        self.operation.connect('draw-page', self._on__draw)

    def _on__begin_print(self, operation, print_context):
        self.doc = self.html._get_document(None, enable_hinting=False)
        self.pages = self.doc.render_pages()
        operation.set_n_pages(len(self.pages))

    def _on__draw(self, operation, print_context, page_no):
        context = print_context.get_cairo_context()
        draw_page(self.pages[page_no], context,
                  enable_hinting=self.doc.enable_hinting,
                  get_image_from_uri=self.doc.get_image_from_uri)

    def run(self, action):
        return self.operation.run(action)
