# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class my_app1(models.Model):
#     _name = 'my_app1.my_app1'
#     _description = 'my_app1.my_app1'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
