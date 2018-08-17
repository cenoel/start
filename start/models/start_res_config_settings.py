# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    """Active multi warehouse et suivi par lot pendant l'install du module"""
    @api.model
    def execute_config(self):
        config_id = self.env['res.config.settings'].search([], limit=1, order='id desc')
        if config_id:
            config_rec = self.env['res.config.settings'].browse(config_id.id)
            config_rec.write({
                'group_stock_multi_locations': True,
                'group_stock_multi_warehouses': True,
                'group_stock_production_lot': True,
                'group_product_variant': True,
            })
            config_rec.execute()
        else:
            config_params = self.env['res.config.settings'].create({})
            config_params.write({
                'group_stock_multi_locations': True,
                'group_stock_multi_warehouses': True,
                'group_stock_production_lot': True,
                'group_product_variant': True,
            })
            config_params.execute()
