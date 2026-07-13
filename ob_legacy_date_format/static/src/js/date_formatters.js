import {
    formatDate as formatNumericDate,
    formatDateTime as formatNumericDateTime,
} from "@web/core/l10n/dates";
import { localization } from "@web/core/l10n/localization";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { DateTimeField } from "@web/views/fields/datetime/datetime_field";

const formatters = registry.category("formatters");
const originalDateFormatter = formatters.get("date");
const originalDateTimeFormatter = formatters.get("datetime");

function obIsDDMMYYYYDateFormatEnabled() {
    return Boolean(session.ob_enable_ddmmyyyy_date_format);
}

function obFormatDate(value, options = {}) {
    if (obIsDDMMYYYYDateFormatEnabled()) {
        return formatNumericDate(value, options);
    }
    return originalDateFormatter(value, options);
}
obFormatDate.extractOptions = originalDateFormatter.extractOptions;

function obFormatDateTime(value, options = {}) {
    if (!obIsDDMMYYYYDateFormatEnabled()) {
        return originalDateTimeFormatter(value, options);
    }
    if (!value) {
        return "";
    }
    if (options.format) {
        return formatNumericDateTime(value, options);
    }
    if (options.showTime === false) {
        return formatNumericDate(value, options);
    }

    const dateFormat = options.showDate === false ? "" : localization.dateFormat;
    let timeFormat = localization.timeFormat;
    if (!options.showSeconds) {
        timeFormat = timeFormat.replace(/:?ss/, "").replace(/\s+/g, " ").trim();
    }
    const format = [dateFormat, timeFormat].filter(Boolean).join(" ");
    return format ? value.setZone(options.tz || "default").toFormat(format) : "";
}
obFormatDateTime.extractOptions = originalDateTimeFormatter.extractOptions;

formatters.add("date", obFormatDate, { force: true });
formatters.add("datetime", obFormatDateTime, { force: true });

patch(DateTimeField.prototype, {
    getFormattedValue(valueIndex, numeric = this.props.numeric) {
        if (!obIsDDMMYYYYDateFormatEnabled()) {
            return super.getFormattedValue(valueIndex, numeric);
        }

        const values = this.values;
        const value = values[valueIndex];
        if (!value) {
            return "";
        }
        const { showSeconds, showTime } = this.props;
        if (this.field.type === "date") {
            return obFormatDate(value);
        }

        const showDate =
            !showTime || valueIndex !== 1 || !values[0] || !values[0].hasSame(value, "day");
        return obFormatDateTime(value, {
            showSeconds,
            showTime,
            showDate,
        });
    },
});
