import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	frappe.reload_doc("real_estate", "doctype", "real_estate_settings")
	frappe.reload_doc("real_estate", "doctype", "property_booking_order")

	rename_field("Real Estate Settings", "property_uom", "property_transaction_uom")
	rename_field("Property Booking Order", "mobile_no", "contact_mobile")
	rename_field("Property Booking Order", "phone_no", "contact_phone")
