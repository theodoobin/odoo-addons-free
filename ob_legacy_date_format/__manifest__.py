# -*- coding: utf-8 -*-

{
    "name": "Legacy Date Format",
    "version": "19.0.1.0.4",
    "category": "Extra Tools",
    "summary": "Show dates as DD/MM/YYYY in Odoo 19",
    "description": """
        Adds a General Settings option to restore the DD/MM/YYYY date format
        for all Odoo languages and standard backend date fields.
    """,
    "author": "theOdooBin",
    "license": "LGPL-3",
    "depends": [
        "base_setup",
        "web",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            (
                "after",
                "web/static/src/views/fields/formatters.js",
                "ob_legacy_date_format/static/src/js/date_formatters.js",
            ),
        ],
    },
    "images": [
        "static/description/cover.png",
        "static/description/date_format_settings.png",
    ],
    "currency": "USD",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
    "application": False,
    "auto_install": False,
}
