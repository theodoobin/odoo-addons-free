# -*- coding: utf-8 -*-

{
    "name": "Inventory Stock Ageing",
    "version": "19.0.1.1.0",
    "category": "Inventory/Inventory",
    "summary": "Analyse remaining inventory by age in a downloadable pivot report",
    "description": """
Inventory Stock Ageing
======================
Shows the current remaining stock split into ageing buckets. A set-based
PostgreSQL query keeps generation responsive for large product catalogs.
The report opens as a pivot table and can be downloaded as an XLSX file
using Odoo's standard pivot download option.
    """,
    "author": "theOdooBin",
    "license": "LGPL-3",
    "depends": [
        "stock_account",
    ],
    "data": [
        "security/ob_stock_ageing_security.xml",
        "security/ir.model.access.csv",
        "views/ob_stock_ageing_views.xml",
    ],
    "images": [
        "static/description/cover.gif",
        "static/description/cover.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
