# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CaracteristicaItem(models.Model):
    _name = "caracteristica.item"
    _rec_name = 'item_id'
    _sql_constraints = [('unique_cat_item', 'UNIQUE (categoria_id, item_id)',
                         'Já existe essa caracteristica, mané!'), ]

    categoria_id = fields.Many2one(
        comodel_name='categoria.caracteristica',
        string='Categoria',
    )

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item',
    )

    parametro_ids = fields.Many2many(
        comodel_name='parametro.caracteristica',
        string='Parâmetros',
    )

    de = fields.Float(
        string='De',
    )

    ate = fields.Float(
        string='Até',
    )


class CategoriaCaracteristica(models.Model):
    _name = 'categoria.caracteristica'
    _rec_name = 'name'
    _sql_constraints = [('unique_cat_name', 'UNIQUE (name)',
                         'Vai botar essa categoria de novo?!'), ]

    name = fields.Char(
        string='Nome',
        required=True,
    )


class ParametroCaracteristica(models.Model):
    _name = 'parametro.caracteristica'
    _rec_name = 'name'
    _sql_constraints = [('unique_param_name', 'UNIQUE (name)',
                         'Em vez de cadastrar esse parâmetro, '
                         'pq não usa o que já existe com o mesmo nome?! =/'), ]

    name = fields.Char(string='Nome')
