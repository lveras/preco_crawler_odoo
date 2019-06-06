# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


def do_signup(self, qcontext):
    """ Shared helper that creates a res.partner out of a token """
    values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'cpf')}
    if not values:
        raise UserError(_("The form was not properly filled in."))
    if values.get('password') != qcontext.get('confirm_password'):
        raise UserError(_("Passwords do not match; please retype them."))
    supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
    if request.lang in supported_langs:
        values['lang'] = request.lang
    self._signup_with_values(qcontext.get('token'), values)
    request.env.cr.commit()

AuthSignupHome.do_signup = do_signup