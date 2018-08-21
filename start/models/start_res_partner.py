# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta
import random
STRING_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
STRING_DIGITAL = '0123456789'

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type_partner = fields.Many2one('start.type.partner',string='Type of partner')
    location_id = fields.Many2one('stock.location',string='Location')
    project_ids = fields.One2many('project.project','patient_id',string='Folders')
    qty_folder = fields.Float('Folders',compute='_set_qty_folder')

    @api.multi
    @api.depends('project_ids')
    def _set_qty_folder(self):
        result_count = self.env['project.project'].search([('patient_id','=',self.id)])
        self.qty_folder = len(result_count)


    @api.model
    def create(self, values):
        patient_partner = super(ResPartner, self).create(values)
        if patient_partner.type_partner.id == self.env.ref('start.start_patient_partner').id:
            check_code = self.env['stock.warehouse'].search([('code','=',patient_partner.name[0:5])])
            if check_code:
                pass
            else:
                result_code = str(self._generateCode())
                warehouse_ref = self.env['stock.warehouse'].create({
                    'name': patient_partner.name,
                    'code': result_code+'_'+patient_partner.name,
                })
                patient_partner.location_id = warehouse_ref.lot_stock_id.id
        return patient_partner

    def _generateCode(self):
        chars = STRING_LETTERS + STRING_DIGITAL
        result = ''.join((random.choice(chars)) for x in range(5))

        return result