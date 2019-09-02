# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Comodo(models.Model):
    _name = "comodo"
    _rec_name = 'name'

    name = fields.Char(
        string='Nome',
        requered=True,
    )

    item_ids = fields.One2many(
        comodel_name='item',
        inverse_name='comodo_id',
        string='Itens',
    )
