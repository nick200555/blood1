# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

app_name = "bloodbank"
app_title = "Bloodbank"
app_publisher = "BloodBank Team"
app_description = "Comprehensive Blood Bank Management System for ERPNext"
app_email = "admin@bloodbank.org"
app_license = "mit"
required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bloodbank/css/bloodbank.css"
# app_include_js = "/assets/bloodbank/js/bloodbank.js"

# include js, css files in header of web template
# web_include_css = "/assets/bloodbank/css/bloodbank.css"
# web_include_js = "/assets/bloodbank/js/bloodbank.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bloodbank/public/scss/website"

# include js, css files in header of web form
# webform_include_css = "/assets/bloodbank/css/bloodbank.css"
# webform_include_js = "/assets/bloodbank/js/bloodbank.js"

# include js in page
# page_js = {"page_name" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ---------
# app_include_icons = "bloodbank/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"bloodbank.jinja_filters.get_blood_stock_status",
		"bloodbank.jinja_filters.get_donor_eligibility_status",
		"bloodbank.jinja_filters.format_blood_group"
	]
}

# Installation
# ------------

# before_install = "bloodbank.install.before_install"
after_install = "bloodbank.setup.install.after_install"

# Uninstallation
# --------------

# before_uninstall = "bloodbank.uninstall.before_uninstall"
# after_uninstall = "bloodbank.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bloodbank.utils.before_app_install"
# after_app_install = "bloodbank.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bloodbank.utils.before_app_uninstall"
# after_app_uninstall = "bloodbank.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bloodbank.notifications.get_notification_config"

# Permissions
# -----------
# Permissions and Grouping by Role
# role_permissions = {
# 	"Donor": {
# 		"read": 1,
# 		"write": 1,
# 		"create": 1,
# 		"delete": 1,
# 		"role": "Blood Bank Manager"
# 	}
# }

# DocType Class Overrides
# -----------------------
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Blood Unit": {
		"after_save": "bloodbank.document_events.update_inventory_on_save"
	},
	"Blood Collection": {
		"before_insert": "bloodbank.document_events.validate_donor_eligibility"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"bloodbank.scheduler.update_donor_eligibility",
		"bloodbank.scheduler.send_donation_reminders",
		"bloodbank.scheduler.generate_daily_collection_summary"
	],
	"hourly": [
		"bloodbank.scheduler.check_expiring_blood_units",
		"bloodbank.scheduler.check_low_stock_levels"
	],
	"weekly": [
		"bloodbank.scheduler.generate_weekly_analytics"
	]
}

# Testing
# -------

# before_tests = "bloodbank.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bloodbank.event.get_events"
# }
#
# each method should be in the format 'link_to_method': 'method_to_override'

# Default Log Clearing
# --------------------
# log_clearing_config = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# API Endpoints
# --------------
# api = {
#     "methods": [
#         "bloodbank.api.donor_api.get_available_donors",
#         "bloodbank.api.inventory_api.get_blood_stock"
#     ]
# }

# Fixtures
# --------
fixtures = [
	{"doctype": "Role", "filters": [["name", "in", ["Blood Bank Manager", "Blood Bank Technician", "Blood Bank Receptionist", "Blood Donor Coordinator", "Hemovigilance Officer"]]]},
	{"doctype": "Custom Field", "filters": [["module", "=", "Bloodbank"]]},
	{"doctype": "Property Setter", "filters": [["module", "=", "Bloodbank"]]}
]
