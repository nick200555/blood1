# Copyright (c) 2025, BloodBank Team and contributors

import frappe

def update_inventory_on_save(doc, method):
    """Triggered by Blood Unit after_save"""
    from bloodbank.utils import auto_update_inventory
    auto_update_inventory()

def validate_donor_eligibility(doc, method):
    """Triggered by Blood Collection before_insert"""
    donor = frappe.get_doc("Donor", doc.donor)
    if not donor.is_eligible:
        frappe.throw(f"Donor {donor.full_name} is currently ineligible to donate. Deferral reason: {donor.deferral_reason or 'Unknown'}")
