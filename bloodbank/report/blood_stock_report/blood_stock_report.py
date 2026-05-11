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
    return columns, data

def get_columns():
    return [
        {"fieldname": "branch", "label": _("Branch"), "fieldtype": "Link", "options": "Blood Bank Branch", "width": 150},
        {"fieldname": "blood_group", "label": _("Blood Group"), "fieldtype": "Link", "options": "Blood Group", "width": 120},
        {"fieldname": "component_type", "label": _("Component Type"), "fieldtype": "Link", "options": "Blood Component Type", "width": 150},
        {"fieldname": "total_units", "label": _("Total Units"), "fieldtype": "Int", "width": 100},
        {"fieldname": "available_units", "label": _("Available"), "fieldtype": "Int", "width": 100},
        {"fieldname": "reserved_units", "label": _("Reserved"), "fieldtype": "Int", "width": 100},
        {"fieldname": "expired_units", "label": _("Expired"), "fieldtype": "Int", "width": 100},
        {"fieldname": "discarded_units", "label": _("Discarded"), "fieldtype": "Int", "width": 100},
        {"fieldname": "minimum_stock", "label": _("Min Stock"), "fieldtype": "Int", "width": 100},
        {"fieldname": "stock_status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "days_supply", "label": _("Days Supply"), "fieldtype": "Int", "width": 100}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("branch"):
        conditions += f" AND branch = '{filters.get('branch')}'"
    if filters.get("blood_group"):
        conditions += f" AND blood_group = '{filters.get('blood_group')}'"
    if filters.get("component_type"):
        conditions += f" AND component_type = '{filters.get('component_type')}'"
    if filters.get("stock_status"):
        conditions += f" AND stock_status = '{filters.get('stock_status')}'"

    query = f"""
        SELECT 
            branch,
            blood_group,
            component_type,
            total_units,
            available_units,
            reserved_units,
            expired_units,
            discarded_units,
            minimum_stock,
            stock_status,
            ROUND(available_units / NULLIF(
                (SELECT AVG(daily_usage) FROM 
                    (SELECT COUNT(*) as daily_usage 
                     FROM `tabBlood Issue` bi 
                     JOIN `tabBlood Issue Item` bii ON bi.name = bii.parent
                     WHERE bii.blood_group = `tabBlood Inventory`.blood_group 
                     AND bii.component_type = `tabBlood Inventory`.component_type
                     AND bi.issue_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                     GROUP BY bi.issue_date) t), 0), 0) as days_supply
        FROM `tabBlood Inventory`
        WHERE 1=1 {conditions}
        ORDER BY branch, blood_group, component_type
    """

    return frappe.db.sql(query, as_dict=True)
