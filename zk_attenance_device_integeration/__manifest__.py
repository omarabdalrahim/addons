# -*- coding: utf-8 -*-
{
    'name': "Zk Attendance Integeration",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    "author": "Mohamed AbdElrahman",
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'data/cron.xml',
        'views/res_company.xml',
         'views/hr_attandanc_views.xml'
    ],

}
