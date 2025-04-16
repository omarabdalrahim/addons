# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import UserError



class HrInfraction(models.Model):
    _name = 'hr.infraction'
    _description = "Hr Infraction"
    _inherit = ['mail.thread', 'image.mixin']

    name = fields.Char(string="Infraction")
    date = fields.Date(string="Date", default=fields.Date.today())
    # date = fields.Date(string="Date", default=fields.Date.today(), readonly=True, states={'draft': [('readonly', False)]})
    period_month = fields.Char(
        string="Period Month", compute="_dynamic_month")
    # readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string="Stage", track_visibility='onchange')
    line_ids = fields.One2many(comodel_name='hr.infraction.line', inverse_name='infraction_id',
                               string="Lines")

    # "Lines", readonly=True, states={'draft': [('readonly', False)]})

    def _change_state(self, state):
        self.write({'state': state})
        for line in self.line_ids:
            line.write({'state': state})

    def action_confirm(self):
        for action in self:
            action._change_state('confirm')

    def action_cancel(self):
        for action in self:
            action._change_state('cancel')

    def action_reset(self):
        for action in self:
            action._change_state('draft')

    def unlink(self):
        for rec in self:
            if rec.state == 'confirm':
                raise UserError(_("You can't delete confirmed records!!!"))
        return super(HrInfraction, self).unlink()

    @api.depends('date')
    def _dynamic_month(self):
        for rec in self:
            if rec.date:
                rec.period_month = rec.date.strftime("%B")
            else:
                rec.period_month = False



