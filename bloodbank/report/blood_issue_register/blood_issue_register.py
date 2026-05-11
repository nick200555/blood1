# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _

@frappe.whitelist()
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "issue_id", "label": _("Issue ID"), "fieldtype": "Link", "options": "Blood Issue", "width": 120},
        {"fieldname": "issue_date", "label": _("Issue Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "healthcare_institution", "label": _("Institution"), "fieldtype": "Link", "options": "Healthcare Institution", "width": 150},
        {"fieldname": "patient_name", "label": _("Patient"), "fieldtype": "Data", "width": 150},
        {"fieldname": "blood_group", "label": _("Blood Group"), "fieldtype": "Link", "options": "Blood Group", "width": 100},
        {"fieldname": "component_type", "label": _("Component"), "fieldtype": "Link", "options": "Blood Component Type", "width": 120},
        {"fieldname": "units_issued", "label": _("Units"), "fieldtype": "Int", "width": 80},
        {"fieldname": "total_amount", "label": _("Amount"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "payment_status", "label": _("Payment"), "fieldtype": "Data", "width": 100},
        {"fieldname": "issued_by", "label": _("Issued By"), "fieldtype": "Link", "options": "User", "width": 120}
    ]

def get_data(filters):
    conditions = " WHERE bi.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND bi.issue_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND bi.issue_date <= '{filters.get('to_date')}'"
    if filters.get("healthcare_institution"):
        conditions += f" AND bi.healthcare_institution = '{filters.get('healthcare_institution')}'"
    if filters.get("blood_group"):
        conditions += f" AND bii.blood_group = '{filters.get('blood_group')}'"

    query = f"""
        SELECT 
            bi.name as issue_id,
            bi.issue_date,
            bi.healthcare_institution,
            bi.patient_name,
            bii.blood_group,
            bii.component_type,
            COUNT(bii.name) as units_issued,
            bi.total_amount,
            bi.payment_status,
            bi.issued_by
        FROM `tabBlood Issue` bi
        JOIN `tabBlood Issue Item` bii ON bi.name = bii.parent
        {conditions}
        GROUP BY bi.name, bii.blood_group, bii.component_type
        ORDER BY bi.issue_date DESC
    """
    return frappe.db.sql(query, as_dict=True)
