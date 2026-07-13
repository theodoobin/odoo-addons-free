# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLegacyDateFormat(TransactionCase):

    def _save_settings(self, enabled):
        settings = self.env["res.config.settings"].create(
            {"ob_enable_ddmmyyyy_date_format": enabled}
        )
        settings.execute()

    def test_setting_applies_and_restores_original_date_format(self):
        language = self.env.ref("base.lang_en")
        original_date_format = language.date_format

        self._save_settings(True)
        self.assertEqual(language.date_format, "%d/%m/%Y")

        self._save_settings(False)
        self.assertEqual(language.date_format, original_date_format)

    def test_new_language_uses_ddmmyyyy_when_setting_is_enabled(self):
        self._save_settings(True)

        language = self.env["res.lang"].create(
            {
                "name": "OB Test Language",
                "code": "x_OB",
                "iso_code": "x_OB",
                "url_code": "x-ob",
                "active": False,
                "direction": "ltr",
                "date_format": "%Y-%m-%d",
                "time_format": "%H:%M:%S",
                "week_start": "1",
                "grouping": "[3,0]",
                "decimal_point": ".",
                "thousands_sep": ",",
            }
        )

        self.assertEqual(language.date_format, "%d/%m/%Y")
