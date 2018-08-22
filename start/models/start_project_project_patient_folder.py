# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo import tools
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

LISTE_CHOIX = [
    ('oui_spontane', 'Oui - Spontané'),
    ('oui_recherche', 'Oui - Recherché'),
    ('non', 'Non'),
    ('nsp', 'NSP')
]


class ProjectProject(models.Model):
    _inherit = 'project.project'

    maintenance_equipment_ids = fields.Many2many(
        'maintenance.equipment',
        string='Parametre machine',
        required=True
    )
    patient_id = fields.Many2one('res.partner','Linked patient',required=True)
    patient_location_ref = fields.Many2one('stock.location',related='patient_id.location_id', readonly=True, store=True)
    state_attachment = fields.Selection([
        ('not_paired', 'Not paired'),
        ('paired_not_transferred', 'Paired not transferred'),
        ('paired_transfered', 'Paired transfered')
    ], compute='_set_state_attachment',readonly=True)

    @api.multi
    @api.depends('maintenance_equipment_ids')
    def _set_state_attachment(self):
        for line in self:
            check_machine = True
            for machine in line.maintenance_equipment_ids:
                if machine.location_id.id == line.patient_id.location_id.id:
                    pass
                else:
                    check_machine = False

            if len(line.maintenance_equipment_ids) < 1:
                line.state_attachment = 'not_paired'
            else:
                if check_machine == True:
                    line.state_attachment = 'paired_transfered'
                else:
                    line.state_attachment = 'paired_not_transferred'

    @api.onchange('maintenance_equipment_ids')
    def check_update(self):
        origin_id = self._origin
        if origin_id:
            old_maintenance = origin_id.maintenance_equipment_ids
            new_maintenance = self.maintenance_equipment_ids
            deleted_maintenance = old_maintenance - new_maintenance
            if deleted_maintenance:
                for line in deleted_maintenance:
                    if line.location_id.id == self.patient_id.location_id.id:
                        raise UserError(_(
                            """You can not delete this machine named {0} serial number {1} from your file because it is still in your warehouse""".format(
                                line.name, line.serial_no)))







