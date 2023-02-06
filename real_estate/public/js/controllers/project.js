frappe.provide("real_estate");
frappe.provide('erpnext.projects');

real_estate.ProjectControllerExtended = class ProjectController extends erpnext.projects.ProjectController {
	onload() {
		super.onload();
	}

	refresh() {
		this.setup_buttons();
	}

	setup_buttons() {
//		super.setup_buttons();
		var me = this;

		if (!me.frm.is_new() && me.frm.doc.is_real_estate_project) {
			if (me.frm.doc.__onload && me.frm.doc.__onload.valid_project_triggers) {
				$.each(me.frm.doc.__onload.valid_project_triggers || [], function (i, project_trigger) {
					me.frm.add_custom_button(__(project_trigger), () => {
						me.create_trigger(me.frm, project_trigger);
					}, __('Create Trigger'));
				});
			}
		}
	}

	create_trigger(frm, project_trigger) {
		var dialog = new frappe.ui.Dialog({
			title: __("Triggering Invoice"),
			fields: [
				{
					fieldname: "trigger_type", fieldtype: "Link", options: "Property Trigger Type",
					label: "Trigger Type", default: project_trigger, read_only: 1,
				},
				{
					fieldtype: "Column Break"
				},
				{
					fieldname: "trigger_date", fieldtype: "Date", options: "",
					label: "Date", default: '', reqd: 1,
				},
			],
			primary_action_label: 'Create Trigger',
			primary_action(values) {

				frappe.call({
					method: "real_estate.enhancements.project.create_trigger",
					args: {
						project: frm.doc.name,
						project_trigger: values.trigger_type,
						trigger_date: values.trigger_date
					},
					callback: function(r) {
						if (r.message && !r.exc) {

						}
					}
				});
				dialog.hide();
				frm.reload_doc();
			}
		});
		dialog.show();
	}
 };

extend_cscript(cur_frm.cscript, new real_estate.ProjectControllerExtended({frm: cur_frm}));
