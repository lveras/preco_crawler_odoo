# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):

    _inherit = "res.users"

    cpf = fields.Char(
        string='CPF',
        related="partner_id.cpf",
    )

    @api.model
    def create(self, vals):
        print('oba')
        return super(ResUsers, self).create(vals)