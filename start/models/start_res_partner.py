# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type_partner = fields.Many2one('start.type.partner',string='Type of partner')