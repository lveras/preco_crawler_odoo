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
        string='Melhor preço encontrado(und)',
    )

    name = fields.Char(
        string='Nome',
    )

    item_id = fields.Many2one(
        comodel_name='item',
        string='Item'
    )

    comodo_id = fields.Many2one(
        comodel_name='comodo',
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

    quantidade = fields.Integer(
        string='Quantidade',
        default=1,
    )

    importancia = fields.Selection(
        selection=[('1', '1'), ('2', '2'), ('3', '3'),
                   ('4', '4'), ('5', '5')],
        string='Importância',
    )

    total_preco = fields.Float(
        string='Valor total',
        compute='_compute_melhor_preco',

    )

    valor_frete = fields.Float(
        string='Valor do Frete',
    )

    @api.model
    def create(self, vals):
        if 'comodo_id' not in vals:
            item_id = self.env['item'].browse(vals['item_id'])
            vals['comodo_id'] = item_id.comodo_id.id

        return super(Produto, self).create(vals)

    @api.depends('quantidade', 'melhor_preco', 'valor_frete')
    def _compute_melhor_preco(self):
        self.total_preco = (self.quantidade*self.melhor_preco) +\
                           self.valor_frete

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
