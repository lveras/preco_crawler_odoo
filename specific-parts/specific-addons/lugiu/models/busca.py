# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Busca(models.Model):
    _name = "busca"

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
