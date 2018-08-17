# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StartTypePartner(models.Model):
    _name = 'start.type.partner'

    name = fields.Char('Name of type partner')
