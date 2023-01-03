# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PropertyUnit(Document):
	def validate(self):
		self.set_title()

	def set_title(self):
		self.title = "-".join(filter(None, [self.unit_number, self.block]))

	def update_status(self, booking_order, update=False, booked=True):
		bookings_for_this_unit = frappe.db.get_all('Property Booking Order', {'property_unit': self.name, 'name': ['!=', booking_order]})
		if bookings_for_this_unit:
			frappe.throw(_('Property Unit Already Booked'))

		if booked:
			self.booking_status = 'Booked'
		else:
			self.booking_status = 'Available'

		if update:
			self.db_set('booking_status', self.booking_status)
