from odoo import fields, models, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    terminal_alias = fields.Char(string="Device Name")
