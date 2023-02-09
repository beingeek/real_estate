# Copyright (c) 2023, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PropertyTriggerType(Document):
	def validate(self):
		self.linked_doc_message()

	def linked_doc_message(self):
		projects = self.get_linked_projects()
		pbos = self.get_linked_pbos()

		linked_doc_string = []
		if projects:
			linked_doc_string.append('<br>'.join(projects))

		if pbos:
			linked_doc_string.append('<br>'.join(pbos))

		if linked_doc_string:
			frappe.throw(_('Cannot modify this Property Type is linked with following: <br>{0}').format('<br>'.join(linked_doc_string)))

	def get_linked_projects(self):
		projects = frappe.get_all('Property Trigger Table', {'trigger_type': self.name}, ['parent', 'parenttype'])
		if projects:
			projects = [d.parent for d in projects]
			links = []
			for d in projects:
				links.append(frappe.get_desk_link("Project", d))
			return links

	def get_linked_pbos(self):
		pbo = frappe.qb.DocType('Property Booking Order')
		ppp = frappe.qb.DocType('Property Payment Plan')
		ppt = frappe.qb.DocType('Payment Plan Type')
		ptt = frappe.qb.DocType('Property Trigger Type')
		pbos = (
			frappe.qb.from_(pbo)
				.inner_join(ppp).on(pbo.name == ppp.parent).inner_join(ppt).on(ppt.name == ppp.payment_plan_type)
				.inner_join(ptt).on(ptt.name == ppt.trigger_type).select(pbo.name)
				.where(ptt.name == self.name).distinct().orderby(pbo.name)
		).run(as_dict=True)

		if pbos:
			pbos = [d.name for d in pbos]
			links = []
			for d in pbos:
				links.append(frappe.get_desk_link("Property Booking Order", d))

			return links


def get_valid_project_triggers():
	project_triggers = frappe.get_all('Property Trigger Type', fields=["name"], filters={"is_project_trigger": 1})
	if project_triggers:
		return [d.name for d in project_triggers]
