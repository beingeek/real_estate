import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	frappe.reload_doc("real_estate", "doctype", "property_unit")
	frappe.reload_doc("real_estate", "doctype", "unit_template")
	frappe.reload_doc("real_estate", "doctype", "property_booking_order")
	frappe.reload_doc("real_estate", "doctype", "property_payment_plan")

	rename_field("Property Booking Order", "type", "property_type")
	rename_field("Property Unit", "type", "property_type")
	rename_field("Unit Template", "type", "property_type")

	rename_field("Property Unit", "land_area_unit", "area_unit")
	rename_field("Unit Template", "land_area_unit", "area_unit")

	rename_field("Property Unit", "land_area", "area")
	rename_field("Unit Template", "land_area", "area")

	rename_field("Property Unit", "rooms", "bedrooms")
	rename_field("Unit Template", "rooms", "bedrooms")

	rename_field("Property Unit", "is_corner_field", "is_corner")
	rename_field("Unit Template", "is_corner_field", "is_corner")

	rename_field("Property Unit", "location", "address")
	rename_field("Unit Template", "location", "address")

	rename_field("Property Payment Plan", "no_of_installment", "no_of_installments")

	for old_name in frappe.get_all("Unit Template", pluck="name"):
		new_name = frappe.db.get_value("Unit Template", old_name, "template_name")
		if old_name != new_name:
			frappe.rename_doc("Unit Template", old_name, new_name, force=True)
