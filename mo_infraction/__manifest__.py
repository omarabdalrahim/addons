{
    "name": "Infraction",
    "author": "Mohamed Elaraby",
    "category": "Human Resources",
    'license': 'LGPL-3',
    "depends": ["base", 'hr', 'mail', 'hr_payroll', 'hr_work_entry_contract_enterprise'],
    "data": [
        "security/ir.model.access.csv",
        "data/tags_data.xml",
        "data/infraction_data.xml",
        "views/mo_infraction_view.xml",
        "views/patient_tag_view.xml",
        "views/hr_infraction.xml",
        "views/hr_payslip_view_inherit.xml",
    ],
    'application': True,
}
