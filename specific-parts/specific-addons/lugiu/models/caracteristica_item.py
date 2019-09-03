# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CaracteristicaItem(models.Model):
    _name = "caracteristica.item"
    _rec_name = 'name'

    name = fields.Char(
        string='Caracteristica',
        default=False,
    )

    de = fields.Float(
        string='De',
    )

    ate = fields.Float(
        string='Até',
    )

    parametro = fields.Char(
        string='Parâmetro',
    )

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item',
    )
