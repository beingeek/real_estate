# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe, erpnext
from frappe import _
from frappe.utils import cstr, getdate, flt, add_to_date, today
from erpnext.controllers.accounts_controller import AccountsController
from real_estate.real_estate.doctype.property_payment_plan_template.property_payment_plan_template import get_payment_plan
from frappe.model.document import Document
import json
from six import string_types


force_fields = [
	'floor', 'type', 'total_price', 'unit_number'
]

dont_update_if_missing = [

]


class PropertyBookingOrder(Document):
	def validate(self):
		if self.get("_action") != "update_after_submit":
			self.set_missing_values()

		self.validate_property_unit_already_booked()
		self.set_payment_plan()
		self.set_payment_plan_dates()
		self.validate_payment_plan()
		self.set_payment_schedule()
		self.validate_payment_schedule()

	def set_missing_values(self, for_validate=False):
		self.set_property_unit_details()

	def on_submit(self):
		self.update_property_unit()
		self.trigger_invoices_on_booking_order()

	def on_cancel(self):
		self.update_property_unit()

	def trigger_invoices_on_booking_order(self):
		for payment in self.payment_schedule:
			plan_type = frappe.get_cached_doc('Payment Plan Type', payment.payment_plan_type)
			if plan_type.get('trigger_on_booking_order'):
				create_sales_invoice(self.name, payment.name)

	def validate_property_unit_already_booked(self):
		filters = {'property_unit': self.property_unit, 'docstatus': 1}
		if not self.is_new():
			filters['name'] = ['!=', self.name]

		existing_booking = frappe.db.exists("Property Booking Order", filters)
		if existing_booking:
			frappe.throw(_('Property Unit is already booked by {0}').format(
				frappe.get_desk_link("Property Booking Order", existing_booking)))

	def set_payment_plan(self):
		if self.payment_plan_template and not self.payment_plan:
			payment_plan = get_payment_plan(self.payment_plan_template)
			for d in payment_plan:
				self.append("payment_plan", d)

	def set_payment_plan_dates(self):
		for plan in self.payment_plan:
			plan_type = frappe.get_cached_doc('Payment Plan Type', plan.payment_plan_type)
			if plan_type.get('trigger_on_booking_order'):
				plan.start_date = self.transaction_date

	@frappe.whitelist()
	def validate_payment_plan(self):
		if not self.payment_plan:
			frappe.throw(_('Payment Plan not set.'))

		self.validate_payment_plan_dates()
		self.validate_payment_plan_amount()

	def validate_payment_plan_dates(self):
		for plan in self.get("payment_plan"):
			if plan.start_date and getdate(plan.start_date) < getdate(self.transaction_date):
				frappe.throw(_("Row #{0}: Payment Plan Due Date cannot be before Booking Date").format(plan.idx))

	def validate_payment_plan_amount(self):
		payment_plan_price_total = flt(sum([flt(plan.invoice_amount) for plan in self.payment_plan]),
			self.precision("total_price"))

		if flt(self.total_price) != payment_plan_price_total:
			frappe.throw(_("Payment Plan Total {0} does not match with Booking Total Price {1}").format(
				frappe.bold(frappe.format(payment_plan_price_total, df=self.meta.get_field("total_price"))),
				frappe.bold(frappe.format(self.total_price, df=self.meta.get_field("total_price")))
			))

	def set_payment_schedule(self):
		payment_schedule = get_payment_schedule(self.payment_plan)
		self.payment_schedule = []
		for d in payment_schedule:
			self.append("payment_schedule", d)

	def validate_payment_schedule(self):
		if not self.payment_schedule:
			frappe.throw(_('Payment Schedule not set.'))
			pass

		self.validate_payment_schedule_dates()

	def validate_payment_schedule_dates(self):
		for plan in self.get("payment_schedule"):
			if not plan.due_date:
				frappe.throw(_("Due Date in Payment Plan missing in Row # {}").format(plan.idx))

			if plan.due_date and getdate(plan.due_date) < getdate(self.transaction_date):
				frappe.throw(_("Row #{0}: Payment Plan Due Date cannot be before Booking Date").format(plan.idx))

	def set_property_unit_details(self):
		property_unit_details = get_property_unit_details(self.property_unit)
		for k, v in property_unit_details.items():
			if self.meta.has_field(k) and (not self.get(k) or k in force_fields) and k not in dont_update_if_missing:
				self.set(k, v)

	def update_property_unit(self):
		property_unit = frappe.get_doc('Property Unit', self.property_unit)
		property_unit.set_status(update=True)
		property_unit.notify_update()


@frappe.whitelist()
def get_payment_schedule(payment_plan):
	if not payment_plan:
		return

	if isinstance(payment_plan, string_types):
		payment_plan = json.loads(payment_plan)

	payment_schedule = []

	for d in payment_plan:
		if d.start_date:
			payment_schedule.extend(get_payment_schedule_rows(d))

	payment_schedule = sorted(payment_schedule, key=lambda d: d.due_date)

	return payment_schedule


def get_payment_schedule_rows(payment_plan):
	payment_schedule = []
	payment_schedule_dict = frappe._dict({
		"payment_plan_row": payment_plan.name,
		"payment_plan_type": payment_plan.payment_plan_type,
	})
	if payment_plan.is_installment and payment_plan.no_of_installment > 1:
		payment_plan.installment_start_date = payment_plan.start_date
		for installment in range(1, payment_plan.no_of_installment + 1):
			plan = payment_schedule_dict.copy()
			plan.is_installment = 1
			plan.due_date = get_installment_date(payment_plan, installment)
			plan.description = '{0} {1}'.format(payment_plan.payment_plan_type, installment)
			plan.invoice_amount = flt(payment_plan.invoice_amount) / flt(payment_plan.no_of_installment)

			payment_schedule.append(plan)

	else:
		plan = payment_schedule_dict.copy()
		plan.due_date = payment_plan.start_date
		plan.description = payment_plan.payment_plan_type
		plan.invoice_amount = flt(payment_plan.invoice_amount)
		payment_schedule.append(plan)

	return payment_schedule


def get_installment_date(payment_plan, installment):
	if not (payment_plan and installment):
		return

	data = dict()
	invoice_interval_count = flt(payment_plan.invoice_interval_count)
	if payment_plan.invoice_interval == 'Day':
		data['days'] = invoice_interval_count * 1
	elif payment_plan.invoice_interval == 'Week':
		data['days'] = invoice_interval_count * 7
	elif payment_plan.invoice_interval == 'Month':
		data['months'] = invoice_interval_count
	elif payment_plan.invoice_interval == 'Year':
		data['years'] = invoice_interval_count

	if installment == 1:
		start_date = payment_plan.start_date
	else:
		start_date = add_to_date(payment_plan.installment_start_date, **data)
		payment_plan.installment_start_date = start_date

	return start_date


@frappe.whitelist()
def get_property_unit_details(property_unit):
	if not property_unit:
		return

	property_unit = frappe.get_cached_doc('Property Unit', property_unit)

	out = frappe._dict({
		'type': property_unit.type,
		'floor': property_unit.floor,
		'total_price': property_unit.price,
		'unit_number': property_unit.unit_number
	})

	return out


@frappe.whitelist()
def make_sales_invoice(property_booking_order, schedule_row_name):
	booking_doc = frappe.get_doc("Property Booking Order", property_booking_order, for_update=True)
	schedule_row = booking_doc.getone("payment_schedule", filters={"name": schedule_row_name})
	if not schedule_row:
		frappe.throw(_("Invalid Payment Schedule reference"))

	invoice = frappe.new_doc('Sales Invoice')
	property_settings = frappe.get_cached_doc('Property Settings')

	invoice.set_posting_time = 1
	invoice.company = booking_doc.company
	invoice.customer = booking_doc.customer
	invoice.property_booking_order = booking_doc.name
	invoice.payment_schedule_row = schedule_row.name
	invoice.property_unit = booking_doc.property_unit
	invoice.posting_date = schedule_row.due_date

	transaction_item = frappe.get_cached_value("Payment Plan Type", schedule_row.payment_plan_type, "transaction_item")

	# Item
	pbo_item = {'item_code': transaction_item, 'qty': 1, 'rate': schedule_row.invoice_amount}
	invoice.append('items', pbo_item)

	# Taxes
	if property_settings.tax_template:
		invoice.taxes_and_charges = property_settings.tax_template

	validate_duplicate_booking_payment_schedule(invoice)

	invoice.run_method("set_missing_values")
	invoice.run_method("reset_taxes_and_charges")
	invoice.run_method("calculate_taxes_and_totals")

	return invoice


@frappe.whitelist()
def create_sales_invoice(property_booking_order, schedule_row_name):
	sales_invoice = make_sales_invoice(property_booking_order, schedule_row_name)
	sales_invoice.save()
	# sales_invoice.submit()


def process_scheduled_installments(date=None):
	if not date:
		date = today()

	installments = get_all_due_installments(date)
	for d in installments:
		create_sales_invoice(d.property_booking_order, d.schedule_row_name)


def get_all_due_installments(date):
	pps = frappe.qb.DocType('Property Payment Schedule')
	pbo = frappe.qb.DocType('Property Booking Order')
	return (
		frappe.qb.from_(pps)
			.inner_join(pbo).on(pbo.name == pps.parent)
			.select(
				pbo.name.as_("property_booking_order"), pps.name.as_("schedule_row_name")
			)
			.where(pps.is_installment == 1).where(pps.due_date <= date)
			.orderby(pbo.name).orderby(pps.due_date)
	).run(as_dict=True)


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


def validate_sales_invoice(doc, method):
	validate_duplicate_booking_payment_schedule(doc)


def validate_duplicate_booking_payment_schedule(doc):
	if not doc.get("property_booking_order") and doc.get("payment_schedule_row"):
		return

	filters = {
		'property_booking_order': doc.property_booking_order,
		'payment_schedule_row': doc.payment_schedule_row,
		'docstatus': ["<", 2]
	}
	if not doc.is_new():
		filters['name'] = ['not in', doc.name]

	invoice_exist = frappe.db.get_all('Sales Invoice', filters=filters)
	if invoice_exist:
		frappe.throw(_('Invoice duplication against this Order'))
