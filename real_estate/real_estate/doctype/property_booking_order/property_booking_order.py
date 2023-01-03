# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PropertyBookingOrder(Document):
	def validate(self):
		self.validate_property_unit_booking_status()

	def on_submit(self):
		self.update_property_unit(booked=True)

	def on_cancel(self):
		self.update_property_unit(booked=False)

	def validate_property_unit_booking_status(self):
		unit_booked = frappe.db.exists('Property Unit', {
			'name': self.property_unit,
			'booking_status': 'Booked'
		})
		if unit_booked:
			frappe.throw(_('Property Unit Already Booked'))

	def update_property_unit(self, booked):
		property_unit = frappe.get_doc('Property Unit', self.property_unit)
		property_unit.update_status(booking_order=self.name, booked=booked, update=True)
