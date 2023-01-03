# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Block(Document):
	def validate(self):
		self.set_title()

	def set_title(self):
		self.title = "-".join(filter(None, [self.project, self.block]))
