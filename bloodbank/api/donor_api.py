# Copyright (c) 2025, BloodBank Team and contributors

import frappe

@frappe.whitelist(allow_guest=False)
def get_eligible_donors(blood_group=None):
    """Retrieve list of eligible donors, optionally filtered by blood group"""
    filters = {"is_eligible": 1, "donor_status": "Active"}
    if blood_group:
        filters["blood_group"] = blood_group
        
    return frappe.get_all("Donor", filters=filters, fields=["name", "full_name", "blood_group", "mobile"])

@frappe.whitelist(allow_guest=False)
def check_blood_availability(blood_group, component_type):
    """Check available units for a specific group and component"""
    available_units = frappe.db.sql("""
        SELECT SUM(available_units) 
        FROM `tabBlood Inventory` 
        WHERE blood_group = %s AND component_type = %s
    """, (blood_group, component_type))[0][0] or 0
    
    return available_units
