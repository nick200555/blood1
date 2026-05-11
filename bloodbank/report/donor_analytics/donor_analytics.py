# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _

@frappe.whitelist()
def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"fieldname": "period", "label": _("Period"), "fieldtype": "Data", "width": 120},
        {"fieldname": "new_donors", "label": _("New Donors"), "fieldtype": "Int", "width": 120},
        {"fieldname": "repeat_donors", "label": _("Repeat Donors"), "fieldtype": "Int", "width": 120},
        {"fieldname": "total_donations", "label": _("Total Donations"), "fieldtype": "Int", "width": 120},
        {"fieldname": "deferred_donors", "label": _("Deferred"), "fieldtype": "Int", "width": 100},
        {"fieldname": "retention_rate", "label": _("Retention Rate %"), "fieldtype": "Percent", "width": 140}
    ]

def get_data(filters):
    from_date = filters.get("from_date", frappe.utils.add_months(frappe.utils.today(), -12))
    to_date = filters.get("to_date", frappe.utils.today())

    query = """
        SELECT 
            DATE_FORMAT(collection_date, '%%Y-%%m') as period,
            COUNT(DISTINCT CASE WHEN donor IN (
                SELECT name FROM `tabDonor` 
                WHERE registration_date >= DATE_FORMAT(collection_date, '%%Y-%%m-01')
            ) THEN donor END) as new_donors,
            COUNT(DISTINCT CASE WHEN donor NOT IN (
                SELECT name FROM `tabDonor` 
                WHERE registration_date >= DATE_FORMAT(collection_date, '%%Y-%%m-01')
            ) THEN donor END) as repeat_donors,
            COUNT(*) as total_donations,
            COUNT(DISTINCT CASE WHEN docstatus = 1 AND name IN (
                SELECT collection FROM `tabDonor Health Screening` 
                WHERE is_eligible = 0
            ) THEN donor END) as deferred_donors
        FROM `tabBlood Collection`
        WHERE collection_date BETWEEN %s AND %s
        AND docstatus = 1
        GROUP BY DATE_FORMAT(collection_date, '%%Y-%%m')
        ORDER BY period
    """

    data = frappe.db.sql(query, (from_date, to_date), as_dict=True)

    for row in data:
        total = row.new_donors + row.repeat_donors
        row.retention_rate = (row.repeat_donors / total * 100) if total else 0

    return data

def get_chart(data):
    if not data:
        return None

    labels = [d.period for d in data]
    new_donors = [d.new_donors for d in data]
    repeat_donors = [d.repeat_donors for d in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "New Donors", "values": new_donors},
                {"name": "Repeat Donors", "values": repeat_donors}
            ]
        },
        "type": "bar",
        "colors": ["#FF6B6B", "#4ECDC4"]
    }
