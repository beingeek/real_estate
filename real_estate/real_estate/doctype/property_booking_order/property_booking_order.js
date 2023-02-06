// Copyright (c) 2022, ParaLogic and contributors
// For license information, please see license.txt

frappe.provide("real_estate");

real_estate.PropertyBookingOrder = class PropertyBookingOrder extends frappe.ui.form.Controller {
	refresh() {
		erpnext.hide_company();
		this.hide_customer_name();
	}

	hide_customer_name() {
		let me = this;
		if (me.frm.customer == me.frm.customer_name) {
			me.frm.toggle_display("customer_name", false);

		}
	}

	payment_plan_template() {
		let me = this;
		if (me.frm.doc.payment_plan_template) {
			if (me.frm.doc.payment_plan) {
				frappe.confirm('Are you sure you want to remake Payment Plan?',
				() => {
					return frappe.call({
						method: "real_estate.real_estate.doctype.property_payment_plan_template.property_payment_plan_template.get_payment_plan",
						args: {
							plan_template: me.frm.doc.payment_plan_template
						},
						callback: function(r) {
							if (r.message && !r.exc) {
								return me.frm.set_value("payment_plan", r.message);
							}
						}
					});
				}, () => { })
			}
		}
	}

	property_unit() {
		let me = this;
		return frappe.call({
			method: "real_estate.real_estate.doctype.property_booking_order.property_booking_order.get_property_unit_details",
			args: {
				property_unit: me.frm.doc.property_unit
			},
			callback: function(r) {
				if (r.message && !r.exc) {
					return me.frm.set_value(r.message);
				}
			}
		});
	}

	validate_payment_plan() {
		let me = this;
		return frappe.call({
			method: "validate_payment_plan",
			doc: me.frm.doc,
			freeze: true,
			freeze_message: "Generating Payment Schedule",
			callback: function(r) {
				if (!r.exc) {
					return me.generate_payment_schedule();
				}
			}
		});
	}

	generate_payment_schedule() {
		let me = this;
		return frappe.call({
			method: "real_estate.real_estate.doctype.property_booking_order.property_booking_order.get_payment_schedule",
			args: {
				payment_plan: me.frm.doc.payment_plan
			},
			callback: function(r) {
				if (r.message && !r.exc) {
					me.frm.set_value("payment_schedule", r.message);
					me.frm.refresh_field('payment_schedule');
				}
			}
		});
	}

	create_invoice(doc, cdt, cdn) {
		let payment_schedule_row = frappe.get_doc(cdt, cdn);

		return frappe.call({
			method: "real_estate.real_estate.doctype.property_booking_order.property_booking_order.make_sales_invoice",
			args: {
				property_booking_order: doc.name,
				schedule_row_name: payment_schedule_row.name
			},
			freeze: true,
			freeze_message: "Creating Invoice",
			callback: function(r) {
				if (r.message && !r.exc) {
					var doc = frappe.model.sync(r.message);
					frappe.set_route("Form", r.message.doctype, r.message.name);
				}
			}
		});
	}

}

extend_cscript(cur_frm.cscript, new real_estate.PropertyBookingOrder({frm: cur_frm}));
