# Copyright (c) 2025, BloodBank Team and contributors

import frappe

def get_blood_stock_status(blood_group, component_type, branch=None):
    filters = {"blood_group": blood_group, "component_type": component_type}
    if branch:
        filters["branch"] = branch
    
    status = frappe.db.get_value("Blood Inventory", filters, "stock_status")
    return status or "Unknown"

def get_donor_eligibility_status(donor):
    is_eligible = frappe.db.get_value("Donor", donor, "is_eligible")
    return "Eligible" if is_eligible else "Deferred"

def format_blood_group(blood_group):
    # Just a pass-through for now, can be used for styling
    return blood_group
