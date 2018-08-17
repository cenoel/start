# -*- coding: utf-8 -*-
from odoo import http

# class Start(http.Controller):
#     @http.route('/start/start/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/start/start/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('start.listing', {
#             'root': '/start/start',
#             'objects': http.request.env['start.start'].search([]),
#         })

#     @http.route('/start/start/objects/<model("start.start"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('start.object', {
#             'object': obj
#         })