# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.osv import expression


class EmployeeNumber(models.Model):
    _name = 'fixed.bonus'
    _description = 'Fixed Bonus'

    name = fields.Char("Fixed Bonus")
    bonus_type = fields.Many2one('hr.bonus.penalty.type', 'Bonus Type')
    bonus_code = fields.Char("Code", related='bonus_type.code', readonly=True)
    amount = fields.Float("Amount")
    note = fields.Char("Note")
    contract_id = fields.Many2one("hr.contract")
