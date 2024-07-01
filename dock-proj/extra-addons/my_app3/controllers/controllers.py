# -*- coding: utf-8 -*-
# from odoo import http


# class MyApp1(http.Controller):
#     @http.route('/my_app1/my_app1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_app1/my_app1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_app1.listing', {
#             'root': '/my_app1/my_app1',
#             'objects': http.request.env['my_app1.my_app1'].search([]),
#         })

#     @http.route('/my_app1/my_app1/objects/<model("my_app1.my_app1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_app1.object', {
#             'object': obj
#         })
