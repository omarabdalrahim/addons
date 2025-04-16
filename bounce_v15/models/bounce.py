from odoo import fields, models, api,_
from odoo.exceptions import UserError


class PayrolStruct(models.Model):
    _inherit = 'hr.payroll.structure'
    is_bounce_deduction = fields.Boolean()


class Bounce(models.Model):
    _name = 'bounce'
    _inherit = ['mail.thread']
    name = fields.Char('Name')
    date = fields.Date('Date', required=True, default=fields.Date.today())
    type = fields.Selection(string='Bounce Based On',
                            selection=[('hour', 'Hour'),
                                       ('day', 'Days'),
                                       ('fixed', 'Fixed'), ], required=True, )
    value = fields.Float('Value')
    bounce_value = fields.Float('Bounce Value', compute="get_bounce_value")
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, )
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    type_id = fields.Many2one('bounce.type')
    note = fields.Text(string="Note")
    # use this field to know it was taken in payslip
    confirmed = fields.Boolean(string='Confirmed', )
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed")], string="State", default='draft')
    @api.onchange('type_id')
    def _onchange_type_id(self):
        self.type = self.type_id.type
        self.value = self.type_id.value

    def confirm(self):
        self.state = 'confirmed'

    def set_draft(self):
        if not self.confirmed:
            self.state = 'draft'

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].get('bounce') or ' '
        return super(Bounce, self).create(values)

    @api.depends('contract_id', 'value', 'type')
    def get_bounce_value(self):
        for rec in self:
            rec.bounce_value = 0
            if rec.type == 'hour':
                rec.bounce_value = rec.value * rec.contract_id.hour_value
            elif rec.type == 'day':
                rec.bounce_value = rec.value * rec.contract_id.day_value
            elif rec.type == 'fixed':
                rec.bounce_value = rec.value


class BounceType(models.Model):
    _name = 'bounce.type'

    name = fields.Char('Name', required=True)
    code = fields.Char('code', required=True)
    type = fields.Selection(string='Bounce Based On',
                            selection=[('hour', 'Hour'),
                                       ('day', 'Days'),
                                       ('fixed', 'Fixed'), ], required=True, )
    struct_ids = fields.Many2many('hr.payroll.structure', string='Struct')
    value = fields.Float('Value')
    _sql_constraints = [
        ('code_uniq', 'unique (code)', "code already exists !"),
    ]

    cat_id = fields.Many2one('hr.salary.rule.category', string="Category")

    @api.model
    def create(self, values):
        res = super(BounceType, self).create(values)
        struct_id = self.env['hr.payroll.structure'].search([('is_bounce_deduction', '=', True)])
        struct_ids = res.struct_ids

        for struct_id in res.struct_ids:

            if not res.cat_id:
                raise UserError(_("Please select a category for the Bounce Type."))

            bounce = self.env['hr.salary.rule'].create({
                'name': res.name,
                'category_id': res.cat_id.id,  # استخدام cat_id
                'code': res.code,
                'sequence': 10,
                'condition_select': 'none',
                'amount_select': 'code',
                'quantity': 1,
                'amount_python_compute': 'if payslip.bounce_line_ids :   result=sum(payslip.bounce_line_ids.filtered(lambda line:line.bounce_id.type_id.code==\'%s\').mapped("bounce_value"))  '
                                         '\nelse:result=0 ' % res.code,
            })
            struct_id.rule_ids = [(4, bounce.id)]
        return res


class bounce_line(models.Model):
    _name = 'bounce.line'

    hr_payslip_id = fields.Many2one(comodel_name='hr.payslip', string='Payslip', )
    bounce_id = fields.Many2one(comodel_name='bounce', string='Bounce', )
    name = fields.Char(string='Type', )
    date = fields.Date(string='Date', )
    notes = fields.Char(string='Notes', )
    bounce_value = fields.Float(string='Value', )


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    bounce_line_ids = fields.One2many(comodel_name='bounce.line', inverse_name='hr_payslip_id', string='Bounes Lines')

    # def V(self):
    #     x=sum(self.bounce_line_ids.filtered(lambda line:line.bounce_id.type_id.id==1).mapped('bounce_value'))
    #     print("D::D:d",x)

    @api.onchange('employee_id', 'date_from', 'date_to', 'payslip_run_id')
    def set_bounce_lines(self):
        for rec in self:
            rec.bounce_line_ids = [(5, 0, 0)]
            lines = []
            emp_bonus = self.env['bounce'].search(
                ['&', '&', '&', '&', ('state', '=', 'confirmed'), ('confirmed', '=', False),
                 ('employee_id', '=', rec.employee_id.id), ('date', '>=', rec.date_from), ('date', '<=', rec.date_to)])
            print("11", emp_bonus)
            for bounce_line in emp_bonus:
                print("1")
                lines.append((0, 0,
                              {'bounce_id': bounce_line.id, 'notes': bounce_line.note, 'name': bounce_line.type_id.name,
                               'date': bounce_line.date, 'bounce_value': bounce_line.bounce_value, }))
            rec.bounce_line_ids = lines

    def compute_sheet(self):
        self.set_bounce_lines()
        res = super(hr_payslip, self).compute_sheet()

        return res

    def action_payslip_done(self):
        res = super(hr_payslip, self).action_payslip_done()
        for bounce_line in self:
            if bounce_line.bounce_line_ids:
                for bounce in bounce_line.bounce_line_ids:
                    print(bounce.bounce_id.confirmed)
                    bounce.bounce_id.confirmed = True
                    print(bounce.bounce_id.confirmed)
        return res
