# -*- coding: utf-8 -*-

{
    "name": "Quick Access Apps",
    "version": "19.0.1.0.1",
    "category": "Extra Tools",
    "summary": "Pin apps into a Quick Access row on the Odoo 19 Enterprise home menu",
    "description": """
        Adds an Enterprise-only Quick Access section to the Odoo 19 home menu,
        allowing users to pin, remove, and reorder frequently used apps.
        Odoo 17 and Odoo 18 require separate version-specific modules.
    """,
    "author": "theOdooBin",
    "license": "LGPL-3",
    "depends": [
        "web_enterprise",
    ],
    "data": [
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ob_quick_access_apps/static/src/js/quick_access_home_menu.js",
            "ob_quick_access_apps/static/src/xml/quick_access_home_menu.xml",
            "ob_quick_access_apps/static/src/scss/quick_access_home_menu.scss",
        ],
    },
    "images": [
        "static/description/quick_access_demo.gif",
        "static/description/cover.png",
        "static/description/quick_access_home_menu.png",
    ],
    "currency": "USD",
    "installable": True,
    "application": False,
    "auto_install": False,
}
