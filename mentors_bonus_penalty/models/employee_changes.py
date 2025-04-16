# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.osv import expression


class EmployeeNumber(models.Model):
    _inherit = 'hr.employee'


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('registration_number', operator, name)]
        employee_ids = self._search(expression.AND([domain, args]), limit=limit)
        return employee_ids