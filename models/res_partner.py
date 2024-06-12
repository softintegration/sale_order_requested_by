# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from psycopg2.errors import ForeignKeyViolation



class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.ondelete(at_uninstall=False)
    def _unlink_if_partner_in_sale_order(self):
        """
        Prevent the deletion of a partner "Individual", child of a company if:
        - partner in 'sale.order'
        - state: all states (draft and posted)
        """
        sale_orders = self.sudo().env['sale.order'].search_count([
            ('requested_by_id', 'in', self.ids)
        ])
        if sale_orders:
            raise UserError(_("The partner cannot be deleted because it is used in Sale orders"))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_partner_in_account_move_as_requested_by(self):
        """
        Prevent the deletion of a partner "Individual", child of a company if:
        - partner in 'account.move'
        """
        moves = self.sudo().env['account.move'].search_count([
            ('requested_by_id', 'in', self.ids)
        ])
        if moves:
            raise UserError(_("The partner cannot be deleted because it is used in Customer invoice"))


    """def unlink(self):
        try:
            res = super().unlink()
            return res
        except ForeignKeyViolation as fkv:
            raise ValidationError(_("Can not remove a Partner related to Sale Order(s)/Account move(s)!"))
        except Exception as ex:
            raise ValidationError(ex)"""