# -*- coding: utf-8 -*-
{
    'name': "Bounce 15",
    'summary': """Bounce V 15""",
    'description': """Bounce""",
    'author': "omar",
    'category': 'HR',
    'depends': ['base', 'hr','payroll'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/bounce.xml',
        'views/bounce_type.xml',
        'views/contract.xml',
    ],
}
