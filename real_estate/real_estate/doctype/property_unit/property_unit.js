// Copyright (c) 2022, ParaLogic and contributors
// For license information, please see license.txt
frappe.provide("real_estate");

real_estate.PropertyUnit = class PropertyUnit extends frappe.ui.form.Controller {
	onload() {
		this.setup_queries();
	}
	setup() {
		this.frm.custom_make_buttons = {
			'Property Booking Order': 'Property Booking Order',
		};
	}

	refresh() {
		erpnext.hide_company();
		this.setup_buttons();
	}

	setup_buttons() {
		if (!this.frm.doc.__islocal && this.frm.doc.status != "Booked") {
			this.frm.add_custom_button(__("Property Booking Order"), () => {
				this.make_property_booking_order();
			}, __("Create"));
		}
	}

	setup_queries() {
		let me = this;
		this.frm.set_query("block", function() {
			return {
				filters:  {
					project: me.frm.doc.project
				}
			};
		});
	}

	make_property_booking_order() {
		frappe.new_doc("Property Booking Order").then(r => {
			cur_frm.set_value("property_unit", this.frm.doc.name);
		});
	}
}

extend_cscript(cur_frm.cscript, new real_estate.PropertyUnit({frm: cur_frm}));
