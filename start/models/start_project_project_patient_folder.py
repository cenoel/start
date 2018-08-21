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
        'patient_folder_equipment_rel',
        'patient_folder_id',
        'equipment_id',
        string='Parametre machine',
        required=True
    )
    patient_id = fields.Many2one('res.partner','Linked patient',required=True)