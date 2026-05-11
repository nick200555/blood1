# Copyright (c) 2025, BloodBank Team and contributors

import frappe
from frappe import _
from frappe.utils import today, date_diff, getdate

@frappe.whitelist()
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "unit_id", "label": _("Unit ID"), "fieldtype": "Link", "options": "Blood Unit", "width": 120},
        {"fieldname": "blood_group", "label": _("Blood Group"), "fieldtype": "Link", "options": "Blood Group", "width": 100},
        {"fieldname": "component_type", "label": _("Component"), "fieldtype": "Link", "options": "Blood Component Type", "width": 120},
        {"fieldname": "collection_date", "label": _("Collection Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "expiry_date", "label": _("Expiry Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "days_remaining", "label": _("Days Remaining"), "fieldtype": "Int", "width": 120},
        {"fieldname": "current_branch", "label": _("Branch"), "fieldtype": "Link", "options": "Blood Bank Branch", "width": 120},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    days = filters.get("days_to_expiry", 7)
    conditions = f" WHERE expiry_date <= DATE_ADD(CURDATE(), INTERVAL {days} DAY)"
    conditions += " AND status IN ('Quarantined', 'Available', 'Reserved')"

    if filters.get("branch"):
        conditions += f" AND current_branch = '{filters.get('branch')}'"
    if filters.get("blood_group"):
        conditions += f" AND blood_group = '{filters.get('blood_group')}'"

    query = f"""
        SELECT name as unit_id, blood_group, component_type, collection_date, expiry_date,
               DATEDIFF(expiry_date, CURDATE()) as days_remaining,
               current_branch, status
        FROM `tabBlood Unit`
        {conditions}
        ORDER BY expiry_date ASC
    """
    data = frappe.db.sql(query, as_dict=True)

    for row in data:
        if row.days_remaining < 0:
            row.days_remaining = 0

    return data
