# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AutomacaoBusca(models.TransientModel):
    _name = "automacao.busca"

    @api.multi
    def executa_buscas(self):
        item_ids = self.env['item'].search(
            [('state', '=', 'pesquisando'),
             ('necessario_buscar', '=', True)])

        for item in item_ids:
            item.buscar()
