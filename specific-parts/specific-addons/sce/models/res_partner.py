# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    _sql_constraints = [
        ('cpf_unique', 'unique(cpf)', 'CPF já cadastrado!')]

    cpf = fields.Char(
        string='CPF',
        requered=True,
    )

    @api.model
    def create(self, vals):
        print('oba')
        return super(ResPartner, self).create(vals)
