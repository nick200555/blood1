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
        {"fieldname": "blood_group", "label": _("Blood Group"), "fieldtype": "Link", "options": "Blood Group", "width": 120},
        {"fieldname": "total_donors", "label": _("Total Donors"), "fieldtype": "Int", "width": 120},
        {"fieldname": "active_donors", "label": _("Active"), "fieldtype": "Int", "width": 100},
        {"fieldname": "deferred_donors", "label": _("Deferred"), "fieldtype": "Int", "width": 100},
        {"fieldname": "first_time_donors", "label": _("First-Time"), "fieldtype": "Int", "width": 100},
        {"fieldname": "repeat_donors", "label": _("Repeat"), "fieldtype": "Int", "width": 100},
        {"fieldname": "retention_rate", "label": _("Retention Rate %"), "fieldtype": "Percent", "width": 140},
        {"fieldname": "avg_donations_per_donor", "label": _("Avg Donations"), "fieldtype": "Float", "width": 120}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("blood_group"):
        conditions += f" AND blood_group = '{filters.get('blood_group')}'"
    if filters.get("from_date"):
        conditions += f" AND registration_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND registration_date <= '{filters.get('to_date')}'"

    query = f"""
        SELECT 
            blood_group,
            COUNT(*) as total_donors,
            SUM(CASE WHEN donor_status = 'Active' THEN 1 ELSE 0 END) as active_donors,
            SUM(CASE WHEN donor_status = 'Deferred' THEN 1 ELSE 0 END) as deferred_donors,
            SUM(CASE WHEN total_donations = 1 THEN 1 ELSE 0 END) as first_time_donors,
            SUM(CASE WHEN total_donations > 1 THEN 1 ELSE 0 END) as repeat_donors,
            ROUND(AVG(total_donations), 1) as avg_donations_per_donor
        FROM `tabDonor`
        WHERE 1=1 {conditions}
        GROUP BY blood_group
        ORDER BY total_donors DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    for row in data:
        total = row.total_donors
        repeat = row.repeat_donors
        row.retention_rate = (repeat / total * 100) if total else 0

    return data
