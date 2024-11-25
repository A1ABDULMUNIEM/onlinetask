{
    'name':'dashboard',
    'author': 'Mn3m',
    'category':'',
    'version':'17.0.0.1.0',
    'depends':[
        'base',
        'sale_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/dashboard_details_menu.xml',

    ],
    'assets': {
        'web.assets_backend': [

        ],
    },
    'application': True
}