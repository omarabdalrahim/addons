from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeNumber(models.Model):
    _inherit = 'hr.employee'

    regist_num = fields.Char(string='Registration Number', required=True)
    pin = fields.Char(string='PIN', required=True)

    @api.onchange('regist_num')
    def _onchange_regist_num(self):
        if self.regist_num:
            self.pin = self.regist_num

    @api.onchange('pin')
    def _onchange_pin(self):
        if self.pin:
            self.regist_num = self.pin

    @api.constrains('regist_num', 'pin')
    def _check_unique_values(self):
        for record in self:
            if self.search_count([('regist_num', '=', record.regist_num), ('id', '!=', record.id)]):
                raise ValidationError("The Registration Number must be unique!")
            if self.search_count([('pin', '=', record.pin), ('id', '!=', record.id)]):
                raise ValidationError("The PIN must be unique!")

    _sql_constraints = [
        ('unique_regist_num', 'unique(regist_num)', 'The Registration Number must be unique!'),
        ('unique_pin', 'unique(pin)', 'The PIN must be unique!')
    ]
