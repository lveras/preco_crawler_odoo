# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Busca(models.Model):
    _name = "busca"

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item',
        requered=True,
    )

    preco = fields.Float(
        string='Preço',
    )

    url = fields.Char(
        string='URL',
    )
