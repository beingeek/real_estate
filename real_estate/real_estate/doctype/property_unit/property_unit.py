# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.controllers.status_updater import StatusUpdater


class PropertyUnit(StatusUpdater):
	def validate(self):
		self.set_status()
		self.validate_block_project()

	def validate_block_project(self):
		block_project = frappe.get_cached_value('Block' ,self.block, 'project')
		if self.project and self.project != block_project:
			frappe.throw(_('Block is not linked with this Project'))

	def set_status(self, update=False, status=None, update_modified=False):
		bookings = frappe.get_all('Property Booking Order', {'property_unit': self.name, 'docstatus': 1})

		if bookings:
			self.booking_status = 'Booked'
		else:
			self.booking_status = 'Available'

		if update:
			self.db_set('booking_status', self.booking_status, update_modified=update_modified)
