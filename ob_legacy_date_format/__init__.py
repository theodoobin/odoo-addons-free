# -*- coding: utf-8 -*-

from . import models


def post_init_hook(env):
    env["res.lang"]._ob_sync_ddmmyyyy_date_format_from_settings()


def uninstall_hook(env):
    env["res.lang"]._ob_restore_original_date_formats()
    env["res.lang"]._ob_clear_date_format_parameters()
