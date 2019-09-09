# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Busca(models.Model):
    _name = "busca"

    confianca = fields.Selection(
        string='Site confiável?',
        selection=[('vai_fundo', 'Vai fundo!'),
                   ('estranho', 'Estranho'),
                   ('corre', 'Mete o pé disso!')]
    )

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item',
        requered=True,
    )

    name = fields.Char(
        string='Nome',
    )

    descricao = fields.Text(
        string='Descrição',
    )

    preco = fields.Float(
        string='Preço',
    )

    url = fields.Html(
        string='URL',
    )
