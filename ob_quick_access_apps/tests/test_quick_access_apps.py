# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestQuickAccessApps(TransactionCase):

    def test_user_setting_stores_quick_access_config(self):
        """Check that the per-user pinned app list is stored unchanged."""
        settings = self.env["res.users.settings"]._find_or_create_for_user(self.env.user)
        value = '["mail.menu_root_discuss"]'

        formatted = settings.set_res_users_settings({"ob_quick_access_config": value})

        self.assertEqual(formatted["ob_quick_access_config"], value)
        self.assertEqual(settings.ob_quick_access_config, value)

    def test_quick_access_preference_is_enabled_by_default(self):
        """Check that Quick Access Apps is enabled for users by default."""
        settings = self.env["res.users.settings"]._find_or_create_for_user(self.env.user)

        self.assertFalse(settings.ob_disable_quick_access_apps)
        self.assertTrue(self.env.user.ob_show_quick_access_apps)

    def test_quick_access_preference_updates_user_settings(self):
        """Check that the user preference updates the backing settings flag."""
        settings = self.env["res.users.settings"]._find_or_create_for_user(self.env.user)

        self.env.user.ob_show_quick_access_apps = False
        self.assertTrue(settings.ob_disable_quick_access_apps)

        self.env.user.ob_show_quick_access_apps = True
        self.assertFalse(settings.ob_disable_quick_access_apps)
