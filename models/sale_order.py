# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    requested_by_id = fields.Many2one('res.partner', 'Requested by', readonly=True, copy=False,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},index=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        self.update({'requested_by_id': False})
        return res

    @api.onchange('requested_by_id')
    def _onchange_requested_by(self):
        if self.requested_by_id and self.partner_id and self.requested_by_id.parent_id.id != self.partner_id.id:
            self.update({'requested_by_id':False})

    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        res.update({'requested_by_id':self.requested_by_id and self.requested_by_id.id})
        return res