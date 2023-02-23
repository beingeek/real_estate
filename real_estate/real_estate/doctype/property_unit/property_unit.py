# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.controllers.status_updater import StatusUpdater


class PropertyUnit(StatusUpdater):
	def validate(self):
		self.validate_block_project()
		self.validate_unit_template_project()
		self.set_status()

	def validate_block_project(self):
		block_project = frappe.get_value('Block' ,self.block, 'project')
		if self.project and self.project != block_project:
			frappe.throw(_('Block is not linked with this Project'))

	def validate_unit_template_project(self):
		unit_template_project = frappe.get_cached_value('Unit Template' ,self.unit_template, 'project')
		if self.project and self.project != unit_template_project:
			frappe.throw(_('Unit Template {0} does not belong to Project {1}').format(self.unit_template, self.project))

	def set_status(self, update=False, status=None, update_modified=False):
		bookings = frappe.get_all('Property Booking Order', {'property_unit': self.name, 'docstatus': 1})

		if bookings:
			self.booking_status = 'Booked'
		else:
			self.booking_status = 'Available'

		if update:
			self.db_set('booking_status', self.booking_status, update_modified=update_modified)

	def set_unit_template_booked_by(self, update=False, status=None, update_modified=False):
		bookings = frappe.get_all('Property Booking Order', fields=["customer"], filters={'property_unit': self.name, 'docstatus': 1})

		if bookings:
			self.booked_by = bookings[0].customer
		else:
			self.booked_by = None

		if update:
			self.db_set('booked_by', self.booked_by, update_modified=update_modified)
