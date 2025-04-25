# -*- coding: utf-8 -*-
{
    'name': "travel_umrah",

    'summary': "Jasa travel umrah",

    'description': """
Perusahaan saya menyediakan travel umrah
    """,

    'author': "MARI UMRAH",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'mail', 'report_xlsx', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sequence_data.xml',
        'views/transaction_travel_package.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_form.xml',
        'report/report_action.xml',
        'report/report_template.xml',
        'views/views.xml',
        'views/menuitem_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

