# -*- coding: utf-8 -*-

import json
import logging

from odoo import api, models
from odoo.tools import str2bool

_logger = logging.getLogger(__name__)

OB_DDMMYYYY_DATE_FORMAT = "%d/%m/%Y"
OB_DATE_FORMAT_SETTING_PARAM = "ob_legacy_date_format.ob_enable_ddmmyyyy_date_format"
OB_ORIGINAL_DATE_FORMATS_PARAM = "ob_legacy_date_format.ob_original_date_formats"


class ResLang(models.Model):
    _inherit = "res.lang"

    @api.model
    def _ob_is_ddmmyyyy_date_format_enabled(self):
        value = self.env["ir.config_parameter"].sudo().get_param(
            OB_DATE_FORMAT_SETTING_PARAM,
            default=False,
        )
        return str2bool(value, False)

    @api.model
    def _ob_get_original_date_formats(self):
        value = self.env["ir.config_parameter"].sudo().get_param(
            OB_ORIGINAL_DATE_FORMATS_PARAM,
            default="{}",
        )
        try:
            data = json.loads(value or "{}")
        except json.JSONDecodeError:
            _logger.warning("Invalid original date format backup; ignoring it.")
            return {}
        return data if isinstance(data, dict) else {}

    @api.model
    def _ob_set_original_date_formats(self, date_formats):
        self.env["ir.config_parameter"].sudo().set_param(
            OB_ORIGINAL_DATE_FORMATS_PARAM,
            json.dumps(date_formats, sort_keys=True),
        )

    @api.model
    def _ob_clear_date_format_parameters(self):
        self.env["ir.config_parameter"].sudo().search(
            [
                (
                    "key",
                    "in",
                    [
                        OB_DATE_FORMAT_SETTING_PARAM,
                        OB_ORIGINAL_DATE_FORMATS_PARAM,
                    ],
                )
            ]
        ).unlink()

    @api.model
    def _ob_sync_ddmmyyyy_date_format_from_settings(self):
        if self._ob_is_ddmmyyyy_date_format_enabled():
            self._ob_apply_ddmmyyyy_date_format()
        else:
            self._ob_restore_original_date_formats()

    @api.model
    def _ob_apply_ddmmyyyy_date_format(self):
        languages = self.sudo().with_context(active_test=False).search([])
        languages._ob_apply_ddmmyyyy_date_format_to_records()

    def _ob_apply_ddmmyyyy_date_format_to_records(self):
        if not self:
            return

        original_date_formats = self._ob_get_original_date_formats()
        backup_changed = False
        for language in self.sudo():
            if language.code not in original_date_formats:
                original_date_formats[language.code] = language.date_format
                backup_changed = True

        if backup_changed:
            self._ob_set_original_date_formats(original_date_formats)

        languages_to_update = self.sudo().filtered(
            lambda language: language.date_format != OB_DDMMYYYY_DATE_FORMAT
        )
        if languages_to_update:
            languages_to_update.with_context(ob_skip_date_format_sync=True).write(
                {"date_format": OB_DDMMYYYY_DATE_FORMAT}
            )
            self.env.registry.clear_cache()

    @api.model
    def _ob_restore_original_date_formats(self):
        original_date_formats = self._ob_get_original_date_formats()
        if not original_date_formats:
            return

        languages = self.sudo().with_context(active_test=False).search(
            [("code", "in", list(original_date_formats))]
        )
        for language in languages:
            original_date_format = original_date_formats.get(language.code)
            if original_date_format and language.date_format != original_date_format:
                language.with_context(ob_skip_date_format_sync=True).write(
                    {"date_format": original_date_format}
                )

        self.env["ir.config_parameter"].sudo().search(
            [("key", "=", OB_ORIGINAL_DATE_FORMATS_PARAM)]
        ).unlink()
        self.env.registry.clear_cache()

    @api.model_create_multi
    def create(self, vals_list):
        languages = super().create(vals_list)
        if (
            not self.env.context.get("ob_skip_date_format_sync")
            and self._ob_is_ddmmyyyy_date_format_enabled()
        ):
            languages._ob_apply_ddmmyyyy_date_format_to_records()
        return languages

    def write(self, vals):
        result = super().write(vals)
        if (
            not self.env.context.get("ob_skip_date_format_sync")
            and self._ob_is_ddmmyyyy_date_format_enabled()
            and {"active", "date_format"} & set(vals)
        ):
            self._ob_apply_ddmmyyyy_date_format_to_records()
        return result
