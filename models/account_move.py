# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    requested_by_id = fields.Many2one('res.partner', 'Requested by', readonly=True, copy=False,
                                      states={'draft': [('readonly', False)]})

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self.update({'requested_by_id': False})
        return res

    @api.onchange('requested_by_id')
    def _onchange_requested_by(self):
        if self.requested_by_id and self.partner_id and self.requested_by_id.parent_id.id != self.partner_id.id:
            self.update({'requested_by_id':False})
