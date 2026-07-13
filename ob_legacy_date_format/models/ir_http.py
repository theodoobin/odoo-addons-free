# -*- coding: utf-8 -*-

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        session_info = super().session_info()
        session_info["ob_enable_ddmmyyyy_date_format"] = (
            self.env["res.lang"]._ob_is_ddmmyyyy_date_format_enabled()
        )
        return session_info
