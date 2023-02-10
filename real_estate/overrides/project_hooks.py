import frappe
from frappe import _
from real_estate.real_estate.doctype.property_trigger_type.property_trigger_type import get_valid_project_triggers
from real_estate.real_estate.doctype.property_booking_order.property_booking_order import get_payment_schedule_rows, create_sales_invoice
from erpnext.projects.doctype.project.project import Project
from frappe.utils import getdate, today


class PropertyProject(Project):
	def onload(self):
		super().onload()
		self.set_onload('valid_project_triggers', get_valid_project_triggers())


@frappe.whitelist()
def create_trigger_row(project, project_trigger, trigger_date=None):
	if not (project and project_trigger):
		return

	if not trigger_date:
		trigger_date = today()

	if frappe.db.exists('Property Trigger Table', {'parent': project, 'parenttype': 'Project',
		'trigger_type': project_trigger, 'trigger_date': trigger_date}):
		frappe.throw(_('Trigger on this date already exist'))

	property_trigger = frappe.new_doc('Property Trigger Table')
	property_trigger.parent = project
	property_trigger.parenttype = 'Project'
	property_trigger.parentfield = 'property_triggers'
	property_trigger.trigger_type = project_trigger
	property_trigger.trigger_date = trigger_date
	property_trigger.insert()

	set_payment_plan_dates_update_schedule(project, project_trigger, trigger_date)


def set_payment_plan_dates_update_schedule(project, property_trigger, trigger_date):
	pbo = frappe.qb.DocType('Property Booking Order')
	ppp = frappe.qb.DocType('Property Payment Plan')
	ppt = frappe.qb.DocType('Payment Plan Type')

	payment_plan_rows = (
		frappe.qb.from_(pbo)
			.inner_join(ppp).on(pbo.name == ppp.parent)
			.inner_join(ppt).on(ppt.name == ppp.payment_plan_type)
			.select(pbo.name.as_('pbo_name'), ppp.payment_plan_type, ppp.name.as_('payment_plan_row_name'))
			.where(ppt.trigger_type == property_trigger)
			.where(pbo.project == project)
			.where(pbo.docstatus == 1)
			.where(ppp.start_date.isnull())
	).run(as_dict=True)

	for d in payment_plan_rows:
		frappe.db.set_value('Property Payment Plan', d.payment_plan_row_name, 'start_date', trigger_date)
		payment_plan_row = frappe.get_cached_doc('Property Payment Plan', d.payment_plan_row_name)
		payment_schedule_rows = get_payment_schedule_rows(payment_plan_row)

		pbo = frappe.get_doc('Property Booking Order', d.pbo_name)
		for payment_schd in payment_schedule_rows:
			new_row = pbo.append('payment_schedule', payment_schd)
			new_row.db_insert()

			if getdate(new_row.due_date) <= getdate(today()):
				create_sales_invoice(new_row.parent, new_row.name)

		if pbo.payment_schedule:
			pbo.payment_schedule = sorted(pbo.payment_schedule, key=lambda d: getdate(d.due_date))
			for i, d in enumerate(pbo.payment_schedule):
				d.idx = i + 1
			pbo.update_child_table("payment_schedule")
