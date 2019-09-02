# -*- coding: utf-8 -*-
from odoo import models, fields, api

IMPORTANCIA = [('indispensavel', 'Indispensável'),
               ('bomter', 'É bom ter'),
               ('perfumaria', 'Perfumaria'),
               ('umdia', 'Um dia, e talvez esse dia nunca chegue...'),]


class Item(models.Model):
    _name = "item"
    _rec_name = 'name'

    name = fields.Char(
        string='Nome',
        requered=True,
    )

    comodo_id = fields.Many2one(
        comodel_name='comodo',
        string='Comodo',
    )

    produto_ids = fields.One2many(
        comodel_name='produto',
        inverse_name='item_id',
        string='Itens',
    )

    quantidade = fields.Integer(
        string='Quantidade',
    )

    importancia = fields.Selection(
        selection=IMPORTANCIA,
        string='Importância',
    )
