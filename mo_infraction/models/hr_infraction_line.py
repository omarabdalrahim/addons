from odoo import models,api,fields


class HrInfractionLine(models.Model):
    _name = 'hr.infraction.line'
    _description = "Hr Infraction Line"
    _rec_name = 'employee_id'

    infraction_id = fields.Many2one(comodel_name='hr.infraction', string="Infraction")
    payslip_id = fields.Many2one(comodel_name='hr.payslip', string="Payslip")
    date = fields.Date(related="infraction_id.date")
    amount_type = fields.Selection(
        [('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days'), ('amount', 'Amount')],
        string="Amount Type"
    )
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True, readonly=False)
    employee_number = fields.Char(string="Employee Number", related='employee_id.registration_number', readonly=False)
    amount = fields.Float("Amount")
    notes = fields.Text("Notes")
    state = fields.Selection( [('draft', 'Draft'),
                               ('confirm', 'Confirmed'),
                               ('done', 'Done'),
                               ('cancel', 'Cancelled')], default='draft', string="Stage", track_visibility='onchange')
    type_id = fields.Many2one(comodel_name="mo.infraction", string="Infraction Type")

    def _compute_other_vals(self, vals_list):
        amount = vals_list.get('amount') or self.amount
        vals_list['amount'] = amount
        return vals_list

    @api.model
    def create(self, vals):
        if vals.get('amount'):
            self._compute_other_vals(vals)
        return super(HrInfractionLine, self).create(vals)

    def write(self, vals_list):
        if vals_list.get('amount'):
            self._compute_other_vals(vals_list)
        return super(HrInfractionLine, self).write(vals_list)
