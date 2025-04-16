
{
    'name': 'Attendance machine integration',

    'version': '17.0',

    'summary': """Integrates Odoo attendance with ZKTeco attendance machines""",
    'description': """This module integrates Odoo attendance with ZKTeco attendance machines
     * This integration was tested with ZKTeco Biopro MV30. For other devices get in touch with us to give you a quick test
        * Integrates biometric device(Face+Thumb) with HR attendance. Tested with ZKTeco Biopro MV30
        * Managing attendance automatically
        * Keeps zk machine history in Odoo
        * Support multiple devices in different locations
        * Clear attendance history on machine from Odoo 
    """,
    'category': 'Human Resources',
    'author': 'IBS',
    'company': 'IBS',
    'website': "https://ibs.com",
    'depends': ['base_setup', 'hr_attendance', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/machine_view.xml',
        'views/machine_attendance_view.xml',
        'views/user_wizard_view.xml',
        'data/download_data.xml', 

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
