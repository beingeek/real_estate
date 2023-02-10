import frappe
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice


class PropertySalesInvoice(SalesInvoice):
	def validate(self):
		super().validate()
		self.validate_duplicate_booking_payment_schedule()

	def on_submit(self):
		super().on_submit()
		self.link_invoice_in_booking_payment_schedule()

	def on_cancel(self):
		super().on_cancel()
		self.unlink_invoice_from_booking_payment_schedule()

	def validate_duplicate_booking_payment_schedule(self):
		if not self.get("property_booking_order") and self.get("payment_schedule_row"):
			return

		filters = {
			'property_booking_order': self.property_booking_order,
			'payment_schedule_row': self.payment_schedule_row,
			'docstatus': ["<", 2]
		}
		if not self.is_new():
			filters['name'] = ['not in', self.name]

		invoice_exist = frappe.db.get_all('Sales Invoice', filters=filters)
		if invoice_exist:
			frappe.throw(_('Invoice duplication against this Order'))

	def link_invoice_in_booking_payment_schedule(self):
		if not self.get("property_booking_order") or not self.get("payment_schedule_row"):
			return

		frappe.db.set_value('Property Payment Schedule', self.payment_schedule_row, 'sales_invoice', self.name)

	def unlink_invoice_from_booking_payment_schedule(self):
		if not self.get("property_booking_order") or not self.get("payment_schedule_row"):
			return

		if frappe.db.exists('Property Payment Schedule', {'name': self.payment_schedule_row, 'sales_invoice': self.name}):
			frappe.db.set_value('Property Payment Schedule', self.payment_schedule_row, 'sales_invoice', None)
			frappe.msgprint(_('Invoice unlinked from {0}').format(
				frappe.get_desk_link("Property Booking Order", self.property_booking_order))
			)
