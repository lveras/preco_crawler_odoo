# -*- coding: utf-8 -*-
{
    'name': "Módulo Usuario",

    'summary': """
        Usuario site
        """,
    'description': """
        SCE
    """,
    'author': "ABGF",
    'website': "http://www.abgf.gov.br",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/auth_signup.xml',
    ],
    'application': True,
}
