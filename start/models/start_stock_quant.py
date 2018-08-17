# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def create(self, values):

        stock_quant = super(StockQuant, self).create(values)
        if stock_quant.product_id:
            check_equipment = self.env['maintenance.equipment'].search([('serial_no','=',stock_quant.lot_id.name)])
            if check_equipment:
                update_equipment = self.env['maintenance.equipment'].browse(check_equipment.id)
                update_equipment.update({
                    'location_id': stock_quant.location_id.id,
                })
            else:
                self.env['maintenance.equipment'].create({
                    'name': stock_quant.product_id.product_tmpl_id.name,
                    'serial_no': stock_quant.lot_id.name,
                    'product_id': stock_quant.product_id.id,
                    'location_id': stock_quant.location_id.id,
                    'lot_id': stock_quant.lot_id.id,
                })
        return stock_quant