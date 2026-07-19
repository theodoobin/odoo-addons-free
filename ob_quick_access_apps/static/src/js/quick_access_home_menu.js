import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { HomeMenu } from "@web_enterprise/webclient/home_menu/home_menu";

const OB_QUICK_ACCESS_SETTING = "ob_quick_access_config";
const OB_QUICK_ACCESS_DISABLED_SETTING = "ob_disable_quick_access_apps";
const OB_QUICK_ACCESS_LIMIT = 8;
const OB_DEFAULT_QUICK_ACCESS_XMLID_GROUPS = [
    ["mail.menu_root_discuss"],
    ["sale.sale_menu_root"],
    ["crm.crm_menu_root"],
    ["stock.menu_stock_root"],
    ["purchase.menu_purchase_root"],
    ["accountant.menu_accounting", "account.menu_finance"],
    ["point_of_sale.menu_point_root"],
    ["contacts.menu_contacts"],
];

/**
 * Parse a user setting value into an ordered list of app XML IDs.
 *
 * @param {string|string[]|null|undefined} value
 * @returns {string[]|null}
 */
function obParseQuickAccessOrder(value) {
    if (Array.isArray(value)) {
        return value;
    }
    if (!value) {
        return null;
    }
    try {
        const parsed = JSON.parse(value);
        return Array.isArray(parsed) ? parsed : null;
    } catch {
        return null;
    }
}

patch(HomeMenu.prototype, {
    /**
     * Initialize Quick Access state from the current user's settings.
     */
    setup() {
        super.setup();
        this.state.obQuickAccessEdit = false;
        this.state.obQuickAccessSaving = false;
        this.state.obQuickAccessOrder = obParseQuickAccessOrder(
            user.settings?.[OB_QUICK_ACCESS_SETTING]
        );
    },

    /**
     * Return the cleaned pinned app XML IDs, falling back to defaults when unset.
     *
     * @returns {string[]}
     */
    get obQuickAccessOrder() {
        if (Array.isArray(this.state.obQuickAccessOrder)) {
            return this._obCleanQuickAccessOrder(this.state.obQuickAccessOrder);
        }
        return this._obGetDefaultQuickAccessOrder();
    },

    /**
     * Return lower-grid apps, excluding apps already shown in Quick Access.
     *
     * @returns {Object[]}
     */
    get displayedApps() {
        const apps = super.displayedApps;
        if (!this.obQuickAccessEnabled) {
            return apps;
        }
        const quickAccessXmlids = new Set(this.obQuickAccessOrder);
        return apps.filter((app) => !quickAccessXmlids.has(app.xmlid));
    },

    /**
     * Resolve pinned app XML IDs to app records visible to the current user.
     *
     * @returns {Object[]}
     */
    get obQuickAccessApps() {
        const appsByXmlid = new Map(this.props.apps.map((app) => [app.xmlid, app]));
        return this.obQuickAccessOrder.map((xmlid) => appsByXmlid.get(xmlid)).filter(Boolean);
    },

    /**
     * Return whether the Quick Access section should be rendered.
     *
     * @returns {boolean}
     */
    get obShouldDisplayQuickAccess() {
        return Boolean(
            this.obQuickAccessEnabled &&
                (this.obQuickAccessApps.length || this.state.obQuickAccessEdit)
        );
    },

    /**
     * Return whether Quick Access is enabled in the current user's preference.
     *
     * @returns {boolean}
     */
    get obQuickAccessEnabled() {
        return !user.settings?.[OB_QUICK_ACCESS_DISABLED_SETTING];
    },

    /**
     * Return whether an app is already pinned in Quick Access.
     *
     * @param {Object} app
     * @returns {boolean}
     */
    obIsQuickAccessApp(app) {
        return this.obQuickAccessOrder.includes(app.xmlid);
    },

    /**
     * Toggle edit mode for adding, removing, and reordering pinned apps.
     */
    async obToggleQuickAccessEdit() {
        if (!this.obQuickAccessEnabled) {
            return;
        }
        this.state.obQuickAccessEdit = !this.state.obQuickAccessEdit;
    },

    /**
     * Add or remove an app from Quick Access depending on its current state.
     *
     * @param {Object} app
     */
    async obToggleAppQuickAccess(app) {
        if (this.obIsQuickAccessApp(app)) {
            await this.obRemoveQuickAccessApp(app);
        } else {
            await this.obAddQuickAccessApp(app);
        }
    },

    /**
     * Add an app to the end of the Quick Access list.
     *
     * @param {Object} app
     */
    async obAddQuickAccessApp(app) {
        const order = this.obQuickAccessOrder;
        if (order.includes(app.xmlid)) {
            return;
        }
        await this._obSaveQuickAccessOrder([...order, app.xmlid]);
    },

    /**
     * Remove an app from the Quick Access list.
     *
     * @param {Object} app
     */
    async obRemoveQuickAccessApp(app) {
        await this._obSaveQuickAccessOrder(
            this.obQuickAccessOrder.filter((xmlid) => xmlid !== app.xmlid)
        );
    },

    /**
     * Move a pinned app left or right within the Quick Access list.
     *
     * @param {Object} app
     * @param {number} direction
     */
    async obMoveQuickAccessApp(app, direction) {
        const order = [...this.obQuickAccessOrder];
        const index = order.indexOf(app.xmlid);
        const nextIndex = index + direction;
        if (index < 0 || nextIndex < 0 || nextIndex >= order.length) {
            return;
        }
        order.splice(index, 1);
        order.splice(nextIndex, 0, app.xmlid);
        await this._obSaveQuickAccessOrder(order);
    },

    /**
     * Restore the Quick Access list to the default visible apps.
     */
    async obResetQuickAccess() {
        this.state.obQuickAccessOrder = null;
        await this._obSaveQuickAccessOrder(this._obGetDefaultQuickAccessOrder());
    },

    /**
     * Build the default Quick Access list from common app XML IDs.
     *
     * @returns {string[]}
     */
    _obGetDefaultQuickAccessOrder() {
        const appXmlids = new Set(this.props.apps.map((app) => app.xmlid));
        const defaultOrder = [];
        for (const xmlids of OB_DEFAULT_QUICK_ACCESS_XMLID_GROUPS) {
            const xmlid = xmlids.find((candidate) => appXmlids.has(candidate));
            if (appXmlids.has(xmlid) && !defaultOrder.includes(xmlid)) {
                defaultOrder.push(xmlid);
            }
            if (defaultOrder.length >= OB_QUICK_ACCESS_LIMIT) {
                break;
            }
        }
        if (defaultOrder.length) {
            return defaultOrder;
        }
        return this.props.apps.slice(0, OB_QUICK_ACCESS_LIMIT).map((app) => app.xmlid);
    },

    /**
     * Remove duplicate or unavailable app XML IDs from a Quick Access list.
     *
     * @param {string[]} order
     * @returns {string[]}
     */
    _obCleanQuickAccessOrder(order) {
        const appXmlids = new Set(this.props.apps.map((app) => app.xmlid));
        const cleanOrder = [];
        for (const xmlid of order || []) {
            if (xmlid && appXmlids.has(xmlid) && !cleanOrder.includes(xmlid)) {
                cleanOrder.push(xmlid);
            }
        }
        return cleanOrder;
    },

    /**
     * Persist a cleaned Quick Access order on the current user's settings.
     *
     * @param {string[]} order
     */
    async _obSaveQuickAccessOrder(order) {
        const cleanOrder = this._obCleanQuickAccessOrder(order);
        this.state.obQuickAccessOrder = cleanOrder;
        this.state.obQuickAccessSaving = true;
        try {
            await user.setUserSettings(OB_QUICK_ACCESS_SETTING, JSON.stringify(cleanOrder));
        } finally {
            this.state.obQuickAccessSaving = false;
        }
    },
});
