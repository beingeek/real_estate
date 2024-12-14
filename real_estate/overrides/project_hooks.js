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
			me.frm.add_custom_button("Create Property Units", function() {
				me.create_property_units(me.frm);
			});
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
					method: "real_estate.overrides.project_hooks.create_trigger_row",
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

	create_property_units(frm) {
		let dialog = new frappe.ui.Dialog({
			title: __("Create Property Units"),
			size: "extra-large",
			fields: [
				{
					fieldname: "unit_template", fieldtype: "Link", label: "Unit Template",
					options: "Unit Template", default: frm.doc.unit_template, reqd: 1,
				},
				{
					fieldname: "payment_plan_template", fieldtype: "Link", label: "Payment Plan Template",
					options: "Property Payment Plan Template", default: frm.doc.payment_plan_template
				},
				{
					fieldtype: "Column Break"
				},

				{
					fieldname: "no_of_units", fieldtype: "Int", label: "No. of Units",
					default: 1, reqd: 1,
				},
				{
					fieldname: "add_property_units", fieldtype: "Button", label: "Add Property Units"
				},
				{
					fieldtype: "Section Break"
				},
				{
					fieldname: "property_units", fieldtype: "Table", label: "Property Units", reqd: 1, 
					fields: [

						{
							fieldname: "unit_number",
							fieldtype: "Data",
							label: "Unit Number",
							in_list_view: 1,
							reqd: 1,
						},
						{
							fieldname: "unit_template",
							fieldtype: "Link",
							label: "Unit Template",
							options: "Unit Template"
						},

						{
							fieldname: "property_type",
							fieldtype: "Link",
							label: "Property Type",
							options: "Property Type",
							reqd: 1
						},
						{
							fieldname: "company",
							fieldtype: "Link",
							label: "Company",
							options: "Company",
							reqd: 1
						},
						{
							fieldtype: "Column Break"
						},
						{
							fieldname: "project",
							fieldtype: "Link",
							label: "Project",
							options: "Project"
						},
						{
							fieldname: "block",
							fieldtype: "Link",
							in_list_view: 1,
							label: "Block",
							options: "Block",
							reqd: 1
						},
						{
							fieldname: "floor",
							fieldtype: "Link",
							in_list_view: 1,
							label: "Floor",
							options: "Floor",
							reqd: 1
						},
						{
							fieldname: "features_section",
							fieldtype: "Section Break",
							label: "Features"
						},
						{
							fieldname: "area_unit",
							fieldtype: "Link",
							label: "Area Unit",
							options: "UOM",
							reqd: 1
						},
						{
							fieldname: "area",
							fieldtype: "Float",
							label: "Area",
							in_list_view: 1,
							non_negative: 1,
							reqd: 1
						},
						{
							fieldtype: "Column Break"
						},
						{
							fieldname: "facing",
							fieldtype: "Select",
							label: "Facing",
							options: "\nNorth\nEast\nWest\nSouth"
						},
						{
							fieldname: "is_road_side",
							fieldtype: "Check",
							label: "Is Road Side",
						},
						{
							fieldname: "is_corner",
							fieldtype: "Check",
							label: "Is Corner",
						},
						{
							fieldtype: "Section Break",
						},
						{
							fieldname: "price",
							fieldtype: "Currency",
							label: "Price",
							in_list_view: 1,
							non_negative: 1,
							reqd: 1
						},
						{
							fieldname: "payment_plan_template",
							fieldtype: "Link",
							label: "Payment Plan Template",
							options: "Property Payment Plan Template"
						}
					],
					data: [],
				},
			],
			primary_action(values) {
				frappe.call({
					method: "real_estate.overrides.project_hooks.create_property_units",
					args: {
						property_units: values.property_units
					},
					callback: function(r) {
						if (r.message && !r.exc) {

						}
					}
				});
				dialog.hide();
				frm.reload_doc();
			},
			primary_action_label: __('Create')
		});

		dialog.get_input("add_property_units").on("click", function () {
			let unit_template = dialog.get_value("unit_template");
			let no_of_units = dialog.get_value("no_of_units");
			let payment_plan_template = dialog.get_value("payment_plan_template");

			frappe.db.get_doc("Unit Template", unit_template).then(unit_template_doc => {
				for (let i = 0; i < no_of_units; i++) {
					let unit_number = i + 1;
					dialog.fields_dict.property_units.df.data.push({
						unit_template: unit_template,
						unit_number: frm.doc.project_name + "-" + unit_template_doc.property_type + "-" + unit_number,
						property_type: unit_template_doc.property_type,
						company: frm.doc.company,
						project: frm.doc.name,
						area_unit: unit_template_doc.area_unit,
						area: unit_template_doc.area,
						facing: unit_template_doc.facing,
						is_road_side: unit_template_doc.is_road_side,
						is_corner: unit_template_doc.is_corner,
						price: unit_template_doc.price,
						payment_plan_template: payment_plan_template
					});
				}
				dialog.fields_dict.property_units.grid.refresh();
			});
		});
		dialog.show();
	}

 };

extend_cscript(cur_frm.cscript, new real_estate.PropertyProjectController({frm: cur_frm}));
