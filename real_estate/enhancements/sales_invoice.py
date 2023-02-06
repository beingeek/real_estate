import frappe
from frappe import _
from real_estate.real_estate.doctype.property_booking_order.property_booking_order import (
	validate_duplicate_booking_payment_schedule
)


def validate_sales_invoice(doc, method):
	validate_duplicate_booking_payment_schedule(doc)


def link_sales_invoice_in_payment_schedule(doc, method):
	if not doc.get("property_booking_order") and doc.get("payment_schedule_row"):
		return

	frappe.db.set_value('Property Payment Schedule', doc.payment_schedule_row, 'sales_invoice', doc.name)
	# frappe.msgprint(_('Invoice linked with Property Booking Order {0}')
	# 	.format(frappe.get_desk_link("Property Booking Order", doc.property_booking_order))
	# )


def unlink_sales_invoice_in_payment_schedule(doc, method):
	if not doc.get("property_booking_order") and doc.get("payment_schedule_row"):
		return

	if doc.payment_schedule_row and frappe.db.exists('Property Payment Schedule', {'name': doc.payment_schedule_row, 'sales_invoice': doc.name}):
		frappe.db.set_value('Property Payment Schedule', doc.payment_schedule_row, 'sales_invoice', '')
		frappe.msgprint(_('Invoice Unlinked from Property Booking Order {0}')
			.format(frappe.get_desk_link("Property Booking Order", doc.property_booking_order))
		)
