# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.osv import expression


class EmployeeNumber(models.Model):
    _inherit = 'hr.contract'

    fixed_bonus_ids = fields.One2many('fixed.bonus', 'contract_id', 'Fixed Bonus')
