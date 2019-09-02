# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Produto(models.Model):
    _name = "produto"
    _rec_name = 'name'

    _sql_constraints = [
        ('item_importancia_unique',
         'unique(item_id, importancia)',
         'Já existe item com essa importância, ô mané!')]

    comprado = fields.Boolean(
        string='Comprado',
        default=False,
    )

    melhor_preco = fields.Float(
        string='Melhor preço encontrado',
    )

    name = fields.Char(
        string='Nome',
    )

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item'
    )

    busca_ids = fields.One2many(
        comodel_name='busca',
        inverse_name='produto_id',
        string='Buscas',
    )

    marca_id = fields.Many2one(
        comodel_name='marca',
        string='Marca',
    )

    importancia = fields.Selection(
        selection=[('1', '1'), ('2', '2'), ('3', '3'),
                   ('4', '4'), ('5', '5')],
        string='Importância',
    )

    @api.multi
    def btn_comprado(self):
        self.comprado = False if self.comprado is True else True


class Marca(models.Model):
    _name = 'marca'

    name = fields.Char(
        string='Nome',
    )

    produto_ids = fields.One2many(
        comodel_name='produto',
        inverse_name='marca_id',
        string='Produtos',
    )
