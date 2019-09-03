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
        compute='_compute_valor_pg',
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
        default=1,
    )

    quant_faltante = fields.Integer(
        string='Faltam comprar',
        compute='_compute_valor_pg',
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
        compute='_compute_valor_pg',
    )

    @api.depends('quantidade', 'produto_ids')
    def _compute_valor_pg(self):
        for rec in self:
            prod_id = rec.produto_ids.filtered(lambda x: x.comprado is True)
            vl_venc = prod_id.melhor_preco
            quant_comprada = prod_id.quantidade
            rec.valor_pg = vl_venc*quant_comprada if vl_venc else 0.0
            rec.quant_faltante = rec.quantidade - quant_comprada
            rec.state = 'comprado' if rec.quant_faltante == 0 \
                else 'pesquisando'

    total_estimado = fields.Float(
        string='Total estimado',
        compute='_compute_total_estimado',
    )

    @api.depends('quantidade', 'valor_estimado')
    def _compute_total_estimado(self):
        for rec in self:
            rec.total_estimado = rec.valor_estimado*rec.quantidade
