# Copyright (c) 2023, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PropertyTriggerType(Document):
	pass


def get_valid_project_triggers():
	project_triggers = frappe.get_all('Property Trigger Type', fields=["name"], filters={"is_project_trigger": 1})
	if project_triggers:
		return [d.name for d in project_triggers]
