from odoo import models, fields, api


class InsuranceTab(models.Model):
    _inherit = "hr.employee"

    social_insurance_no = fields.Char(string="Social Insurance No.")
    social_insurance_date = fields.Date(string="Social Insurance Date")
    insurance_start_date = fields.Date(string="Social Insurance Start")
    insurance_end_date = fields.Date(string="Social Insurance End")
    insurance_amount = fields.Float(string="Insurance Amount")
    company_percentage = fields.Float(string="Company Percentage")
    employee_percentage = fields.Float(string="Employee Percentage")
    employee_share = fields.Float(string="Employee Share", compute='_compute_employee_share')
    company_share = fields.Float(string="Company Share", compute='_compute_company_share')

    @api.depends('insurance_amount', 'employee_percentage')
    def _compute_employee_share(self):
        for rec in self:
            rec.employee_share = rec.insurance_amount * rec.employee_percentage / 100

    @api.depends('insurance_amount', 'company_percentage')
    def _compute_company_share(self):
        for rec in self:
            rec.company_share = rec.insurance_amount * rec.company_percentage / 100
