from odoo import models, fields


class MoInfraction(models.Model):
    _name = "mo.infraction"
    _description = "Mo Infraction"

    name = fields.Char()
    code = fields.Char()
    tag_ids = fields.Many2many(string="Tags", comodel_name="mo.tags")



