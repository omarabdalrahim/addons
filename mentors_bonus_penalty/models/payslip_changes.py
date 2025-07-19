import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from odoo.tools.safe_eval import safe_eval


# Ibrahim Samir Code Start ---->


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    # BONUS PART
    # ####################################################
    def _get_hr_bonuses(self):
        bonus_line_obj = self.env['hr.bonus.penalty.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id),
                          ('state', '=', 'confirm'), ('type', '=', 'bonus')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_bonus_ids': [(6, 0, bonus_line_obj.search(domain).mapped('id'))]})

    hr_bonus_ids = fields.One2many('hr.bonus.penalty.line', 'payslip_id', "Bonuses",
                                   domain=[('type', '=', 'bonus')])
    registration_number = fields.Char("Employee Number", related='employee_id.registration_number')

    def _get_hr_penalties(self):
        penalty_line_obj = self.env['hr.bonus.penalty.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id),
                          ('state', '=', 'confirm'), ('type', '=', 'penalty')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_penalty_ids': [(6, 0, penalty_line_obj.search(domain).mapped('id'))]})

    hr_penalty_ids = fields.One2many('hr.bonus.penalty.line', 'payslip_id', "Penalties",
                                     domain=[('type', '=', 'penalty')])

    @api.onchange('struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        super(HrPayslipInherit, self)
        self._get_hr_bonuses()
        self._get_hr_penalties()

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrPayslipInherit, self).create(vals_list)
        res._get_hr_bonuses()
        res._get_hr_penalties()
        return res

    def action_payslip_done(self):
        """
        Append Function to add extra action action_set_line_confirm
        :return: SUPER
        """
        lines_dicts = [{'lines': self.hr_bonus_ids, 'inverse_name': 'bonus_penalty_id'},
                       {'lines': self.hr_penalty_ids, 'inverse_name': 'bonus_penalty_id'},]
        for lines_dict in lines_dicts:
            self.action_set_line_confirm(lines_dict)
        return super(HrPayslipInherit, self).action_payslip_done()

    def action_set_line_confirm(self, lines_dict):
        """
        Change State of this field lines to done to avoid using it on another payslip
        :param lines_dict: one2many field of those lines
        """
        for line in lines_dict['lines']:
            line.write({'state': 'done'})
            main_field = getattr(line, lines_dict['inverse_name'])
            if all(state == 'done' for state in main_field.line_ids.mapped('state')):
                main_field.write({'state': 'done'})
