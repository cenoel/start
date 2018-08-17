# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_id = fields.Many2one('product.product',string='Product name')
    lot_id = fields.Many2one('stock.production.lot',string='Lot name')
    location_id = fields.Many2one('stock.location',string='Location')
    state = fields.Selection([
        ('unavailable', 'Unavailable'),
        ('available', 'Available'),
        ('patient', 'In patient')
    ], string='State', readonly=True, index=True, default='available')