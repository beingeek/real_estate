from . import __version__ as app_version

app_name = "real_estate"
app_title = "Real Estate"
app_publisher = "ParaLogic"
app_description = "App for Real Estate Automation"
app_email = "info@paralogic.io"
app_license = "GNU General Public License (v3)"
required_apps = ["erpnext"]

doctype_js = {"Project": "overrides/project_hooks.js"}

override_doctype_class = {
	"Project": "real_estate.overrides.project_hooks.PropertyProject",
	"Sales Invoice": "real_estate.overrides.sales_invoice_hooks.PropertySalesInvoice",
}

scheduler_events = {
	"daily": [
		"real_estate.real_estate.doctype.property_booking_order.property_booking_order.process_scheduled_installments"
	],
}

fixtures = [
	{
		'doctype': 'Custom Field',
		"filters": [
			[
				"name", "in",
				[
					"Sales Invoice-property_details", "Sales Invoice-property_unit", "Sales Invoice-cb_property_details_1",
					"Sales Invoice-property_booking_order", "Sales Invoice-payment_schedule_row",
					# "Customer-guardian_type", "Customer-guardian_name",
					"Item-vehicle_allocation_required_from_delivery_period", "Item-payment_plan_type", "Item-is_property_transaction_item",
					"Project-property_details", "Project-is_real_estate_project", "Project-property_triggers"
				]
			]
		]
	},
	{
		'dt': 'DocType Link',
		"filters": [["parent", "=", "Project"], ["parenttype", "=", "Customize Form"], ["custom", "=", "1"]]
	}
]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/real_estate/css/real_estate.css"
# app_include_js = "/assets/real_estate/js/real_estate.js"

# include js, css files in header of web template
# web_include_css = "/assets/real_estate/css/real_estate.css"
# web_include_js = "/assets/real_estate/js/real_estate.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "real_estate/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "real_estate.utils.jinja_methods",
#	"filters": "real_estate.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "real_estate.install.before_install"
# after_install = "real_estate.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "real_estate.uninstall.before_uninstall"
# after_uninstall = "real_estate.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "real_estate.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# Document Events
# ---------------
# Hook on document methods and events

# Scheduled Tasks
# ---------------

# Testing
# -------

# before_tests = "real_estate.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "real_estate.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "real_estate.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"real_estate.auth.validate"
# ]
