# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    ob_show_quick_access_apps = fields.Boolean(
        string="Show Quick Access Apps",
        compute="_compute_ob_show_quick_access_apps",
        inverse="_inverse_ob_show_quick_access_apps",
        groups="base.group_user",
        help="Show the Quick Access Apps section on the Enterprise home menu.",
    )

    @property
    def SELF_READABLE_FIELDS(self):
        """Allow users to read their own Quick Access Apps preference."""
        return super().SELF_READABLE_FIELDS + ["ob_show_quick_access_apps"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        """Allow users to update their own Quick Access Apps preference."""
        return super().SELF_WRITEABLE_FIELDS + ["ob_show_quick_access_apps"]

    @api.depends("res_users_settings_id.ob_disable_quick_access_apps")
    def _compute_ob_show_quick_access_apps(self):
        """Compute the visible preference from the stored disable flag."""
        for user in self:
            user.ob_show_quick_access_apps = (
                not user.res_users_settings_id.ob_disable_quick_access_apps
            )

    def _inverse_ob_show_quick_access_apps(self):
        """Persist the visible preference on the related user settings record."""
        for user in self:
            settings = self.env["res.users.settings"]._find_or_create_for_user(user)
            settings.ob_disable_quick_access_apps = not user.ob_show_quick_access_apps
