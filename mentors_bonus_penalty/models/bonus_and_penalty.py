# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import UserError


# Ibrahim Samir Code Start ---->


class HrBonusPenalty(models.Model):
    _name = 'hr.bonus.penalty'
    _description = "Hr Bonus/Penalty"
    _inherit = ['mail.thread', 'image.mixin']

    name = fields.Char("Bonus/Penalty")

    type = fields.Selection(
        [('bonus', 'Bonus'), ('penalty', 'Penalty')],
        "Type")

    date = fields.Date("Date", default=fields.Date.today())

    period_month = fields.Char("Period Month", compute="_MonthPeriod")

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string="Stage", tracking=True)

    line_ids = fields.One2many('hr.bonus.penalty.line', 'bonus_penalty_id', string="Lines")

    def _MonthPeriod(self):
        for rec in self:
            if rec.date:
                rec.period_month = rec.date.strftime("%B")

    # total_amount_lines = fields.One2many(
    #     'total.amount.line',
    #     'wizard_id',
    #     string='Total Amount Lines'
    # )

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
        return super(HrBonusPenalty, self).unlink()

    # @api.onchange('line_ids')
    # @api.depends('line_ids.amount')
    # def _get_total_bonus_penalty(self):
    #     total = {}
    #     for rec in self:
    #         for line in rec.line_ids:
    #             if line.type_id not in total:
    #                 total.update({line.type_id: [line.amount]})
    #             elif line.type_id in total:
    #                 total.update({line.type_id: total[line.type_id] + line.amount})

            # rec.total_amount_lines.unlink()
            # for key, value in total.items():
            #     rec.total_amount_lines += TotalAmountLine.create({
            #         'wizard_id': rec.id,
            #         'type': key,
            #         'amount': value
            #     })


class TotalAmountLine(models.Model):
    _name = 'total.amount.line'
    _description = 'Total Amount Line'

    wizard_id = fields.Many2one('hr.bonus.penalty')
    type = fields.Char()
    amount = fields.Float()


class HrBonusPenaltyLine(models.Model):
    _name = 'hr.bonus.penalty.line'
    _description = "Hr Bonus/Penalty Line"
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'image.mixin']


    bonus_penalty_id = fields.Many2one('hr.bonus.penalty', "Bonus/Penalty")
    payslip_id = fields.Many2one('hr.payslip', "Payslip")
    date = fields.Date(related='bonus_penalty_id.date')
    amount_type = fields.Selection(
        [('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days'), ('money', 'Money')],
        "Amount Type"
    )
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, readonly=False,)
    employee_number = fields.Char("Employee Number", related='employee_id.registration_number')
    type_id = fields.Many2one('hr.bonus.penalty.type', "Bonus/Penalty Type", required=True)
    type_code = fields.Char("Code", related="type_id.code")
    amount = fields.Float("Amount")
    notes = fields.Text("Notes")

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string="Stage", tracking=True)
    type = fields.Selection(related='bonus_penalty_id.type')

    @api.depends('employee_id')
    def _compute_name_get(self):
        result = []
        for rec in self:
            name = f"{rec.employee_id.registration_number} - {rec.employee_id.name}"
            result.append((rec.id, name))
        return result

    # @api.onchange('employee_id')
    # def onchange_employee(self):
    #     if self.employee_id:
    #         self.employee_registration = self.employee_id.registration_number

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('amount'):
                self._compute_other_vals(vals)
        return super(HrBonusPenaltyLine, self).create(vals_list)

    def write(self, vals_list):
        for line in self:
            if vals_list.get('amount'):
                line._compute_other_vals(vals_list)
            return super(HrBonusPenaltyLine, self).write(vals_list)

    def _compute_other_vals(self, vals_list):
        amount = vals_list.get('amount') or self.amount
        vals_list['amount'] = amount
        return vals_list


class HrBonusPenaltyType(models.Model):
    _name = 'hr.bonus.penalty.type'
    _description = "Hr Bonus Type"

    name = fields.Char("Bonus Type", translate=True)
    type = fields.Selection([('bonus', 'Bonus'),
                             ('penalty', 'Penalty')], "Type")
    code = fields.Char("Code")
