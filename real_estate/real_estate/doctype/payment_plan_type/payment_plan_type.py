# Copyright (c) 2023, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentPlanType(Document):
	def before_insert(self):
		self.create_transaction_item()

	def on_trash(self):
		# validations ?
		self.delete_transaction_item()

	def delete_transaction_item(self):
		self.db_set('transaction_item', '')
		transaction_item = frappe.get_doc('Item', {
			'payment_plan_type': self.plan_name,
			'is_property_transaction_item': 1
		})
		transaction_item.delete()

	def create_transaction_item(self):
		property_settings = frappe.get_cached_doc('Real Estate Settings')

		item_doc = frappe.new_doc('Item')
		item_doc.update({
			'name': self.plan_name,
			'item_code': self.plan_name,
			'item_name': self.plan_name,
			'description': self.description,
			'payment_plan_type': self.plan_name,
			'is_property_transaction_item': 1,
			'is_stock_item': 0,
			'is_purchase_item': 0,
			'is_sales_item': 1,
			'include_item_in_manufacturing': 0,
			'stock_uom': property_settings.property_transaction_uom,
			'uom': property_settings.property_transaction_uom,
			'item_group': property_settings.item_group
		})

		item_doc.save(ignore_permissions=True)
		self.transaction_item = item_doc.name
