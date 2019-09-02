# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Busca(models.Model):
    _name = "busca"

    produto_id = fields.Char(
        string='Produto',
        requered=True,
    )

    preco = fields.Float(
        string='Preço',
    )

    url = fields.Char(
        string='URL',
    )
