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

    # @api.multi
    # def write(self, values):
    #     print(self.patient_id.id)
    #     for line in self:
    #         if 'maintenance_equipment_ids' in values:
    #             for edit in values['maintenance_equipment_ids']:
    #                 print(edit.id)
    #                 print('***********')
    #                 print(line.patient_id.location_id.id)
    #                 if edit.location_id.id == line.patient_id.location_id.id:
    #                     raise UserError(_("""You can not delete this machine named {0} serial number {1} from your file because it is still in your warehouse""".format(edit.name,edit.serial_no)))
    #     return super(ProjectProject, self).write(values)



