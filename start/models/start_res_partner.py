# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type_partner = fields.Many2one('start.type.partner',string='Type of partner')

    @api.model
    def create(self, values):
        patient_partner = super(ResPartner, self).create(values)(self)
        if patient_partner.type_partner.id == self.env.ref('start.start_patient_partner').id:
            self.env[''].create({
                'name':patient_partner.name,
                'code':patient_partner.id + '' +patient_partner.name,
                'partner_id':self.env.uid
            })
        return patient_partner