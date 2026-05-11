# Copyright (c) 2025, BloodBank Team and contributors

import frappe
from frappe import _

@frappe.whitelist()
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "collection_id", "label": _("Collection"), "fieldtype": "Link", "options": "Blood Collection", "width": 120},
        {"fieldname": "collection_date", "label": _("Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "donor", "label": _("Donor"), "fieldtype": "Link", "options": "Donor", "width": 120},
        {"fieldname": "donor_name", "label": _("Donor Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "blood_group", "label": _("Blood Group"), "fieldtype": "Link", "options": "Blood Group", "width": 100},
        {"fieldname": "collection_method", "label": _("Method"), "fieldtype": "Data", "width": 120},
        {"fieldname": "volume_collected_ml", "label": _("Volume mL"), "fieldtype": "Float", "width": 100},
        {"fieldname": "donation_site", "label": _("Site"), "fieldtype": "Link", "options": "Donation Site", "width": 150},
        {"fieldname": "branch", "label": _("Branch"), "fieldtype": "Link", "options": "Blood Bank Branch", "width": 120},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "phlebotomist", "label": _("Phlebotomist"), "fieldtype": "Link", "options": "User", "width": 120}
    ]

def get_data(filters):
    conditions = " WHERE docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND collection_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND collection_date <= '{filters.get('to_date')}'"
    if filters.get("branch"):
        conditions += f" AND branch = '{filters.get('branch')}'"
    if filters.get("blood_group"):
        conditions += f" AND blood_group = '{filters.get('blood_group')}'"
    if filters.get("collection_method"):
        conditions += f" AND collection_method = '{filters.get('collection_method')}'"

    query = f"""
        SELECT name as collection_id, collection_date, donor, donor_name, blood_group,
               collection_method, volume_collected_ml, donation_site, branch, status, phlebotomist
        FROM `tabBlood Collection`
        {conditions}
        ORDER BY collection_date DESC
    """
    return frappe.db.sql(query, as_dict=True)
