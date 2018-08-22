# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_id = fields.Many2one('product.product', string='Product name')
    lot_id = fields.Many2one('stock.production.lot', string='Lot name')
    location_id = fields.Many2one('stock.location', string='Location')
    location_dest_id = fields.Many2one('stock.location', string='Location destination')
    state = fields.Selection([
        ('unavailable', 'Unavailable'),
        ('available', 'Available'),
        ('patient', 'In patient')
    ], string='State', readonly=True, index=True, default='available')
    equipment_image_medium = fields.Binary("Image", compute='_compute_image_equipment')

    @api.one
    @api.depends('product_id')
    def _compute_image_equipment(self):
        self.ensure_one()
        if self.product_id:
            product_template_obj = self.env['product.template'].search([('id', '=', self.product_id.id)])
            self.equipment_image_medium = product_template_obj.image_medium

    def attach_machine(self):
        if self.state == 'patient':
            raise UserError(_('This machine is not available'))
        parent_context_id = self.env.context
        stock_picking_obj = self.env['stock.picking']
        project_ref = self.env['project.project'].search([('id', '=', parent_context_id['project_id'])])
        picking_type_ref = self.env['stock.picking.type'].search(
            ['&', ('name', '=', 'Internal Transfers'), ('warehouse_id.name', '=', project_ref.patient_id.name)])
        product_ref = self.env['product.product'].search([('name', '=', self.name)])
        move_line_name = ''
        if product_ref.product_tmpl_id.default_code:
            move_line_name = '[' + product_ref.product_tmpl_id.default_code + '] '
        move_lines_ref = self.env['stock.move'].create({
            'name': move_line_name + product_ref.product_tmpl_id.name,
            'product_id': product_ref.id,
            'product_uom': 1,
            'location_id': self.location_id.id,
            'location_dest_id': project_ref.patient_id.location_id.id,
            'product_uom_qty': 1
        })
        move_line_ids_ref = self.env['stock.move.line'].create({
            'product_id': product_ref.id,
            'location_id': self.location_id.id,
            'location_dest_id': project_ref.patient_id.location_id.id,
            'lot_id': self.env['stock.production.lot'].search([('name', '=', self.serial_no)]).id,
            'product_uom_id': 1,
            'qty_done': 1
        })
        to_validate = stock_picking_obj.create({
            'location_id': self.location_id.id,
            'location_dest_id': project_ref.patient_id.location_id.id,
            'scheduled_date': min(move_lines_ref.mapped('date_expected')),
            'picking_type_id': picking_type_ref.id,
            'moves_lines': move_lines_ref,
            'move_line_ids': move_line_ids_ref
        })
        move_lines_ref.update({
            'picking_id': to_validate.id
        })
        move_line_ids_ref.update({
            'picking_id': to_validate.id
        })
        to_validate.button_validate()
        to_update_state = self.env['maintenance.equipment'].browse(self.id)
        to_update_state.update({
            'state': 'patient'
        })

    def select_destination_location(self):
        view = self.env.ref('start.start_destination_location_form')
        return {
            'name': _('Destination location'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'equipment.detach',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'project_id':self.env.context['project_id'],'machine_to_detach':self.id},
        }


class DetachMachine(models.Model):
    _name = 'equipment.detach'

    name = fields.Many2one('stock.location', string='Location destination')
    motif_detatch = fields.Text('Reason for detachment machine')

    def detach_machine(self):
        parent_context_id = self.env.context['project_id']
        machine_self = self.env['maintenance.equipment'].search([('id','=',self.env.context['machine_to_detach'])])
        project_ref = self.env['project.project'].search([('id', '=', parent_context_id)])
        if machine_self.location_id.id != project_ref.patient_id.location_id.id:
            raise UserError(_('This machine is not in your folder, you can not detach it'))
        stock_picking_obj = self.env['stock.picking']
        location_destination_ref = self.name.id
        picking_type_ref = self.env['stock.picking.type'].search(
            ['&', ('name', '=', 'Internal Transfers'), ('warehouse_id.name', '=', 'Nurse chest')])
        product_ref = self.env['product.product'].search([('name', '=', machine_self.name)])
        move_line_name = ''
        if product_ref.product_tmpl_id.default_code:
            move_line_name = '[' + product_ref.product_tmpl_id.default_code + '] '
        move_lines_ref = self.env['stock.move'].create({
            'name': move_line_name + product_ref.product_tmpl_id.name,
            'product_id': product_ref.id,
            'product_uom': 1,
            'location_id': machine_self.location_id.id,
            'location_dest_id': location_destination_ref,
            'product_uom_qty': 1
        })
        move_line_ids_ref = self.env['stock.move.line'].create({
            'product_id': product_ref.id,
            'location_id': machine_self.location_id.id,
            'location_dest_id': location_destination_ref,
            'lot_id': self.env['stock.production.lot'].search([('name', '=', machine_self.serial_no)]).id,
            'product_uom_id': 1,
            'qty_done': 1
        })
        to_validate = stock_picking_obj.create({
            'location_id': machine_self.location_id.id,
            'location_dest_id': location_destination_ref,
            'scheduled_date': min(move_lines_ref.mapped('date_expected')),
            'picking_type_id': picking_type_ref.id,
            'moves_lines': move_lines_ref,
            'move_line_ids': move_line_ids_ref
        })
        move_lines_ref.update({
            'picking_id': to_validate.id
        })
        move_line_ids_ref.update({
            'picking_id': to_validate.id
        })
        to_validate.button_validate()
        to_update_state = self.env['maintenance.equipment'].browse(machine_self.id)
        to_update_state.update({
            'state': 'available'
        })
