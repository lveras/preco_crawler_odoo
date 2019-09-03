# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Comodo(models.Model):
    _name = "comodo"
    _rec_name = 'name'

    name = fields.Char(
        string='Nome',
        requered=True,
    )

    indispensavel_total = fields.Float(
        string='Indispensável',
        compute='_compute_indices',
    )

    indispensavel_pg = fields.Float(
        string='Indispensável',
        compute='_compute_indices',
    )

    bomter_total = fields.Float(
        string='Bom ter',
        compute='_compute_indices',
    )

    bomter_pg = fields.Float(
        string='Bom ter',
        compute='_compute_indices',
    )

    perfumaria_total = fields.Float(
        string='Perfumaria',
        compute='_compute_indices',
    )

    perfumaria_pg = fields.Float(
        string='Perfumaria',
        compute='_compute_indices',
    )

    umdia_total = fields.Float(
        string='Talvez nunca chegue',
        compute='_compute_indices',
    )

    umdia_pg = fields.Float(
        string='Talvez nunca chegue',
        compute='_compute_indices',
    )

    item_ids = fields.One2many(
        comodel_name='item',
        inverse_name='comodo_id',
        string='Itens',
    )

    @api.depends('item_ids')
    def _compute_indices(self):
        importancias = ['indispensavel', 'bomter', 'perfumaria', 'umdia']
        for rec in self:
            for importancia in importancias:
                item_ids = rec.item_ids.filtered(
                    lambda x: x.importancia == importancia)
                total = sum([item.valor_pg if item.state == 'comprado' else
                             item.total_estimado for item in item_ids])

                pg = sum(rec.item_ids.filtered(
                    lambda x: x.importancia == importancia).mapped('valor_pg'))

                setattr(rec, '{}_{}'.format(importancia, 'total'), total)
                setattr(rec, '{}_{}'.format(importancia, 'pg'), pg or 1)
