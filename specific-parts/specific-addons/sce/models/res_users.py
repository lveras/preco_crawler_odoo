# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        res.partner_id.cpf = vals['cpf']

        return res
