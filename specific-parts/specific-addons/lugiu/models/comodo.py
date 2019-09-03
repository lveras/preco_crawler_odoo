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

    indispensavel_porcent = fields.Float(
        string='Indispensável',
        compute='_compute_indices',
    )

    bomter_total = fields.Float(
        string='Bom ter',
        compute='_compute_indices',
    )

    bomter_porcent = fields.Float(
        string='Bom ter',
        compute='_compute_indices',
    )

    perfumaria_total = fields.Float(
        string='Perfumaria',
        compute='_compute_indices',
    )

    perfumaria_porcent = fields.Float(
        string='Perfumaria',
        compute='_compute_indices',
    )

    umdia_total = fields.Float(
        string='Talvez nunca chegue',
        compute='_compute_indices',
    )

    umdia_porcent = fields.Float(
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

        for importancia in importancias:
            total = sum(self.item_ids.filtered(
                lambda x: x.importancia == importancia).mapped(
                'valor_estimado'))

            pg = sum(self.item_ids.filtered(
                lambda x: x.importancia == importancia).mapped('valor_pg'))

            percent = (pg * 100) / total if total else 0

            setattr(self, '{}_{}'.format(importancia, 'total'), total)
            setattr(self, '{}_{}'.format(importancia, 'pg'), percent)
