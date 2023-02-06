import frappe
from frappe import _
from real_estate.real_estate.doctype.property_trigger_type.property_trigger_type import get_valid_project_triggers
from erpnext.projects.doctype.project.project import Project
from frappe.utils import today

class PropertyProject(Project):
	def onload(self):
		self.set_onload('valid_project_triggers', get_valid_project_triggers())


@frappe.whitelist()
def create_trigger(project, project_trigger, trigger_date=None):
	if not (project and project_trigger):
		return

	if not trigger_date:
		trigger_date = today()

	if frappe.db.exists('Property Trigger Table', {'parent': project, 'parenttype': 'Project',
		'trigger_type': project_trigger, 'trigger_date': trigger_date}):
		frappe.throw(_('Trigger on this date already exist'))

	doc = frappe.new_doc('Property Trigger Table')
	doc.parent = project
	doc.parenttype = 'Project'
	doc.parentfield = 'property_triggers'
	doc.trigger_type = project_trigger
	doc.trigger_date = trigger_date
	doc.insert()
