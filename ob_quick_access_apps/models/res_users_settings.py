# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    ob_quick_access_config = fields.Json(
        string="Quick Access Apps Configuration",
        readonly=True,
        help="Per-user list of app XML IDs pinned in the Enterprise home menu Quick Access row.",
    )
    ob_disable_quick_access_apps = fields.Boolean(
        string="Disable Quick Access Apps",
        readonly=True,
        help="Hide the Enterprise home menu Quick Access row for this user.",
    )
