# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ob_enable_ddmmyyyy_date_format = fields.Boolean(
        string="Use DD/MM/YYYY Date Format",
        config_parameter="ob_legacy_date_format.ob_enable_ddmmyyyy_date_format",
        help="Display standard Odoo dates as DD/MM/YYYY for all languages.",
    )

    def set_values(self):
        super().set_values()
        self.ensure_one()
        self.env["res.lang"]._ob_sync_ddmmyyyy_date_format_from_settings()
