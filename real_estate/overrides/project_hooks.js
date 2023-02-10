frappe.provide("real_estate");
frappe.provide('erpnext.projects');

real_estate.PropertyProjectController = class PropertyProjectController extends erpnext.projects.ProjectController {
	refresh() {
		super.refresh();
		this.setup_buttons();
	}

	setup_buttons() {
		super.setup_buttons();
		let me = this;

		if (!me.frm.is_new() && me.frm.doc.is_real_estate_project) {
			if (me.frm.doc.__onload && me.frm.doc.__onload.valid_project_triggers) {
				var existing_project_triggers = me.frm.doc.property_triggers.map((p) => p.trigger_type);
				var project_triggers = me.frm.doc.__onload.valid_project_triggers;
				var triggers = project_triggers.filter(x => !existing_project_triggers.includes(x));

				$.each(triggers || [], function (i, property_trigger) {
						me.frm.add_custom_button(__(property_trigger), () => {
							me.create_trigger_row(me.frm, property_trigger);
						}, __('Trigger'));
				});
			}
		}
	}

	create_trigger_row(frm, project_trigger) {
		let dialog = new frappe.ui.Dialog({
			title: __("Create Trigger Row"),
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
			primary_action(values) {
				frappe.call({
					method: "real_estate.enhancements.project.create_trigger_row",
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

extend_cscript(cur_frm.cscript, new real_estate.PropertyProjectController({frm: cur_frm}));
