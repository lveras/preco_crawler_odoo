# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):

    _inherit = "res.partner"

    cpf = fields.Char(
        string='CPF'
    )


    @api.model
    def create(self, vals):
        print('oba')
        return super(ResPartner, self).create(vals)