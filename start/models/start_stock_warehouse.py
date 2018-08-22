# -*- coding: utf-8 -*-
from odoo import models, api


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    @api.model_cr
    def init(self):
        tcode = {
            'Central': 'Central logistician',
            'Inventory': 'Inventory',
            'Agency': 'Agency',
            'Garages': 'Nurse garages',
            'Chest': 'Nurse chest',
        }
        for code, name in tcode.items():
            if not self.is_code_in_base(code):
                self.env['stock.warehouse'].create({
                    'name': name,
                    'code': code,
                })

    @api.model
    def is_code_in_base(self, code_name):
        code_in_base = False
        if self.env['stock.warehouse'].search([('code', '=', code_name[0:5])]):
            code_in_base = True
        return code_in_base
