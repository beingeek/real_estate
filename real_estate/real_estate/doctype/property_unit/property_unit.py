# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.controllers.status_updater import StatusUpdater


class PropertyUnit(StatusUpdater):
	def validate(self):
		self.set_status()

	def set_status(self, update=False, status=None, update_modified=False):
		bookings = frappe.get_all('Property Booking Order', {'property_unit': self.name, 'docstatus': 1})

		if bookings:
			self.booking_status = 'Booked'
		else:
			self.booking_status = 'Available'

		if update:
			self.db_set('booking_status', self.booking_status, update_modified=update_modified)
