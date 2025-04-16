import datetime
from odoo import fields, models, api
import requests
import json
from datetime import datetime, timedelta

class Employee(models.Model):
    _inherit = "hr.employee"

    def get_token(self, company_id):
        url = company_id.zk_url + 'jwt-api-token-auth/'
        payload = json.dumps({
            "username": company_id.zk_username,
            "password": company_id.password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        if 'token' in result:
            return result['token']
        else:
            return ''

    def get_date_employee(self, employee_id, company_id, token):
        url = company_id.zk_url + "iclock/api/transactions/?start_time=%s&end_time=%s&emp_code=%s" % (
            datetime.today().date(), datetime.today().date() + timedelta(days=1), employee_id.pin)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT %s' % (token)
        }
        payload = json.dumps({})

        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()

        if 'data' in result:
            return result['data']

    def generate_api_zk(self):
        for rec in self.search([('pin', '!=', False)]):
            check_in, check_out, terminal_alias = '', '', ''
            if rec.company_id.zk_url or rec.company_id.zk_username or rec.company_id.password:
                token = self.get_token(rec.company_id)
                data = self.get_date_employee(rec, rec.company_id, token)

                try:
                    if data:
                        if 'terminal_alias' in data[0]:
                            terminal_alias = data[0]['terminal_alias']

                        if data[0]['punch_state_display'] == 'Check In':
                            check_in = data[0]['punch_time']
                        if data[1]['punch_state_display'] == 'Check Out':
                            check_out = data[-1]['punch_time']

                        if check_in:
                            if check_out:
                                attend_id = self.env['hr.attendance'].create({
                                    'employee_id': rec.id,
                                    'check_in': datetime.strptime(check_in, '%Y-%m-%d %H:%M:%S') - timedelta(hours=2),
                                    'check_out': datetime.strptime(check_out, '%Y-%m-%d %H:%M:%S') - timedelta(hours=2),
                                    'terminal_alias': terminal_alias,
                                })
                            else:
                                attend_id = self.env['hr.attendance'].create({
                                    'employee_id': rec.id,
                                    'check_in': datetime.strptime(check_in, '%Y-%m-%d %H:%M:%S') - timedelta(hours=2),
                                    'terminal_alias': terminal_alias,
                                })
                except Exception as e:
                    print(e)
