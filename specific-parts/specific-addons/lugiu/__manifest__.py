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
        'views/comodo.xml',
        'views/item.xml',
        'views/busca.xml',
        'views/menu.xml',
        'views/automacao_busca.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}
