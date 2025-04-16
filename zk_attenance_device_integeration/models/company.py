from odoo import fields, models, api


class Company(models.Model):
    _inherit = "res.company"
    zk_url = fields.Char()
    zk_username= fields.Char()
    password = fields.Char()