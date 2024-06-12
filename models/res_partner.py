# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from psycopg2.errors import ForeignKeyViolation



class ResPartner(models.Model):
    _inherit = "res.partner"

    def unlink(self):
        try:
            res = super().unlink()
            return res
        except ForeignKeyViolation as fkv:
            raise ValidationError(_("Can not remove a Partner related to Sale Order(s)/Account move(s)!"))
        except Exception as ex:
            raise ValidationError(ex)