# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_round

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        for line in self:
            for moves in line.move_lines:
                for lots in moves.move_line_ids:
                    chech_stock_location = self.env['stock.quant'].search(['&',('lot_id','=',lots.lot_id.id),('quantity','>',0)])
                    if chech_stock_location.location_id.location_id.name != False:
                        if chech_stock_location.location_id.id != lots.location_id.id:
                            raise UserError(_("""This stock is not in {0} source location but in {1}""".format(lots.location_id.location_id.name,chech_stock_location.location_id.location_id.name)))
        execute_parent_function = super(StockPicking, self).button_validate()

        return execute_parent_function
