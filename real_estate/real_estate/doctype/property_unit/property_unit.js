// Copyright (c) 2022, ParaLogic and contributors
// For license information, please see license.txt
frappe.provide("real_estate");

real_estate.PropertyUnit = class PropertyUnit extends frappe.ui.form.Controller {
	refresh() {
		erpnext.hide_company();
		this.setup_buttons();
	}

	setup_buttons() {
		this.frm.add_custom_button(__("Create Property Booking Order"), () => {
//				this.create_booking_order();
		});
	}
}

extend_cscript(cur_frm.cscript, new real_estate.PropertyUnit({frm: cur_frm}));
