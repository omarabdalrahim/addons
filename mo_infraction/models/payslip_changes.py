from odoo import models, fields, api


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    hr_infraction_ids = fields.One2many(comodel_name='hr.infraction.line', inverse_name='payslip_id')




    def _get_hr_infraction(self):
        infraction_line_obj = self.env['hr.infraction.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id),
                          ('state', '=', 'confirm')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_infraction_ids': [(6, 0, infraction_line_obj.search(domain).mapped('id'))]})

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        # super(HrPayslipInherit, self)._onchange_employee()
        self._get_hr_infraction()

    def action_payslip_done(self):
        """
        Append Function to add extra action action_set_line_confirm
        :return: SUPER
        """
        lines_dicts = [{'lines': self.hr_infraction_ids, 'inverse_name': 'infraction_id'}]
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
