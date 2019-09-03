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
        string='Total - Indispensável',
        compute='_compute_indices',
    )

    indispensavel_porcent = fields.Float(
        string='Progresso',
        compute='_compute_indices',
    )

    bomter_total = fields.Float(
        string='Total - Bom ter',
        compute='_compute_indices',
    )

    bomter_porcent = fields.Float(
        string='Progresso',
        compute='_compute_indices',
    )

    perfumaria_total = fields.Float(
        string='Total - Perfumaria',
        compute='_compute_indices',
    )

    perfumaria_porcent = fields.Float(
        string='Progresso',
        compute='_compute_indices',
    )

    umdia_total = fields.Float(
        string='Total - Talvez nunca chegue',
        compute='_compute_indices',
    )

    umdia_porcent = fields.Float(
        string='Progresso',
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
        res = {importancia: {'total': 0, 'percent': 0}
               for importancia in importancias}

        for importancia in importancias:
            total = sum(self.item_ids.filtered(
                lambda x: x.importancia == importancia).mapped(
                'valor_estimado'))
            pg = sum(self.item_ids.filtered(
            lambda x: x.importancia == importancia).mapped('valor_pg'))

            percent = (pg * 100) / total

            setattr(self, '{}_{}'.format(importancia, 'total'), total)
            setattr(self, '{}_{}'.format(importancia, 'pg'), percent)
