# -*- coding: utf-8 -*-
{
    'name': "lugiu",

    'summary': """
        Lu e Giu
        """,
    'description': """
        Lugiu
    """,
    'author': "Luciano Veras",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/comodo.xml',
        'views/item.xml',
        'views/busca.xml',
        'views/menu.xml',
        'security/security.xml',
    ],
    'application': True,
}
