# -*- coding: utf-8 -*-

from odoo import models, fields, api, _,tools
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", default='serial', required=True)