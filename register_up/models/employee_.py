from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeNumber(models.Model):
    _inherit = 'hr.employee'

    registration_number = fields.Char(string='Registration Number')
    pin = fields.Char(string='PIN')

    @api.onchange('registration_number')
    def _onchange_registration_number(self):
        if self.registration_number:
            self.pin = self.registration_number

    @api.onchange('pin')
    def _onchange_pin(self):
        if self.pin:
            self.registration_number = self.pin

    @api.constrains('registration_number', 'pin')
    def _check_unique_values(self):
        for record in self:
            if self.search_count([('registration_number', '=', record.registration_number), ('id', '!=', record.id)]):
                raise ValidationError("The Registration Number must be unique!")
            if self.search_count([('pin', '=', record.pin), ('id', '!=', record.id)]):
                raise ValidationError("The PIN must be unique!")

    _sql_constraints = [
        ('unique_registration_number', 'unique(registration_number)', 'The Registration Number must be unique!'),
        ('unique_pin', 'unique(pin)', 'The PIN must be unique!')
    ]
