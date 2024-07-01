# -*- coding: utf-8 -*-
# from odoo import http


# class MyApp2(http.Controller):
#     @http.route('/my_app2/my_app2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_app2/my_app2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_app2.listing', {
#             'root': '/my_app2/my_app2',
#             'objects': http.request.env['my_app2.my_app2'].search([]),
#         })

#     @http.route('/my_app2/my_app2/objects/<model("my_app2.my_app2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_app2.object', {
#             'object': obj
#         })
