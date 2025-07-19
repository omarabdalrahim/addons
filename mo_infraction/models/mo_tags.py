from odoo import models, fields


class MoTags(models.Model):
    _name = "mo.tags"
    _description = "Mo Tags"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color 2')

