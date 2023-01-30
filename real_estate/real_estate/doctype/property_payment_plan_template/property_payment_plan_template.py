# Copyright (c) 2023, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, getdate, flt, add_to_date
import json
from six import string_types


class PropertyPaymentPlanTemplate(Document):
	def validate(self):
		self.validate_payment_plan_installment()

	def validate_payment_plan_installment(self):
		for d in self.payment_plan:
			if d.is_installment:
				validate_payment_plan_row_installment(d)
			else:
				d.no_of_installment = ''
				d.invoice_interval = ''
				d.invoice_interval_count = ''


@frappe.whitelist()
def get_payment_plan(plan_template):
	if not plan_template:
		return

	terms_doc = frappe.get_cached_doc("Property Payment Plan Template", plan_template)

	payment_plan = []
	for d in terms_doc.get("payment_plan"):

		payment_plan.append({
			'payment_plan_type': d.payment_plan_type,
			'is_installment': d.is_installment,
			'no_of_installment': d.no_of_installment,
		})
	return payment_plan


@frappe.whitelist()
def validate_payment_plan_row_installment(payment_plan):
	if not payment_plan:
		return

	if isinstance(payment_plan, string_types):
		payment_plan = frappe._dict(json.loads(payment_plan))

	if payment_plan.is_installment:
		message = ''
		if not payment_plan.no_of_installment:
			message += '<li>No of installment</li>'
		if not payment_plan.invoice_interval:
			message +=  '<li>Invoice interval</li>'
		if not payment_plan.invoice_interval_count:
			message += '<li>Invoice interval count</li>'

		if message:
			frappe.throw(_('Mandatory fields required in table <b>Payment Plan</b>, Row {0} <br><br><ul>{1}</ul>').format(payment_plan.idx, message))
