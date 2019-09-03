# -*- coding: utf-8 -*-
from odoo import models, fields, api

IMPORTANCIA = [('indispensavel', 'Indispensável'),
               ('bomter', 'É bom ter'),
               ('perfumaria', 'Perfumaria'),
               ('umdia', 'Um dia, e talvez esse dia nunca chegue...'), ]

STATE = [('pesquisando', 'Pesquisando'),
         ('comprado', 'Comprado'), ]


class Item(models.Model):
    _name = "item"
    _rec_name = 'name'

    name = fields.Char(
        string='Nome',
        requered=True,
    )

    state = fields.Selection(
        string='Status',
        selection=STATE,
        default='pesquisando',
    )

    comodo_id = fields.Many2one(
        comodel_name='comodo',
        string='Comodo',
    )

    quantidade = fields.Integer(
        string='Quantidade',
        default=1,
    )

    quant_faltante = fields.Integer(
        string='Faltam comprar',
    )

    importancia = fields.Selection(
        selection=IMPORTANCIA,
        default='indispensavel',
        string='Importância',
    )

    valor_estimado = fields.Float(
        string='Valor estimado(und)',
    )

    valor_pg = fields.Float(
        string='Valor pago',
    )

    caracteristica_item_ids = fields.One2many(
        comodel_name='caracteristica.item',
        inverse_name='item_id',
        string='Caracteristicas',
    )

    busca_ids = fields.One2many(
        comodel_name='busca',
        inverse_name='item_id',
        string='Buscas',
    )

    total_estimado = fields.Float(
        string='Total estimado',
        compute='_compute_total_estimado',
    )

    @api.depends('quantidade', 'valor_estimado')
    def _compute_total_estimado(self):
        for rec in self:
            rec.total_estimado = rec.valor_estimado*rec.quantidade
