# Copyright (c) 2025, BloodBank Team and contributors

import frappe

def after_install():
    """Seed initial master data"""
    create_blood_groups()
    create_component_types()
    create_deferral_reasons()
    create_donor_types()

def create_blood_groups():
    groups = [
        {"blood_group": "A+", "description": "A Positive"},
        {"blood_group": "A-", "description": "A Negative"},
        {"blood_group": "B+", "description": "B Positive"},
        {"blood_group": "B-", "description": "B Negative"},
        {"blood_group": "AB+", "description": "AB Positive"},
        {"blood_group": "AB-", "description": "AB Negative"},
        {"blood_group": "O+", "description": "O Positive"},
        {"blood_group": "O-", "description": "O Negative"}
    ]
    for g in groups:
        if not frappe.db.exists("Blood Group", g["blood_group"]):
            doc = frappe.get_doc({"doctype": "Blood Group", **g})
            doc.insert(ignore_permissions=True)

def create_component_types():
    components = [
        {"component_name": "Whole Blood", "shelf_life_days": 35, "storage_temperature_range": "2 to 6 C"},
        {"component_name": "Packed Red Cells", "shelf_life_days": 42, "storage_temperature_range": "2 to 6 C"},
        {"component_name": "Fresh Frozen Plasma", "shelf_life_days": 365, "storage_temperature_range": "-18 C or below"},
        {"component_name": "Platelets", "shelf_life_days": 5, "storage_temperature_range": "20 to 24 C"},
        {"component_name": "Cryoprecipitate", "shelf_life_days": 365, "storage_temperature_range": "-18 C or below"}
    ]
    for c in components:
        if not frappe.db.exists("Blood Component Type", c["component_name"]):
            doc = frappe.get_doc({"doctype": "Blood Component Type", **c})
            doc.insert(ignore_permissions=True)

def create_deferral_reasons():
    reasons = [
        {"reason": "Low Hemoglobin", "deferral_type": "Temporary", "deferral_period_days": 30},
        {"reason": "Recent Tattoo", "deferral_type": "Temporary", "deferral_period_days": 180},
        {"reason": "Antibiotics", "deferral_type": "Temporary", "deferral_period_days": 7},
        {"reason": "Low Weight", "deferral_type": "Temporary", "deferral_period_days": 0},
        {"reason": "Positive Infectious Marker", "deferral_type": "Permanent", "deferral_period_days": 0},
        {"reason": "High Risk Behavior", "deferral_type": "Permanent", "deferral_period_days": 0}
    ]
    for r in reasons:
        if not frappe.db.exists("Deferral Reason", r["reason"]):
            doc = frappe.get_doc({"doctype": "Deferral Reason", **r})
            doc.insert(ignore_permissions=True)

def create_donor_types():
    types = [
        {"type_name": "Voluntary", "min_donation_interval_days": 56, "is_voluntary": 1},
        {"type_name": "Replacement", "min_donation_interval_days": 56, "is_replacement": 1},
        {"type_name": "Directed", "min_donation_interval_days": 56, "is_directed": 1},
        {"type_name": "Autologous", "min_donation_interval_days": 7, "is_autologous": 1}
    ]
    for t in types:
        if not frappe.db.exists("Donor Type", t["type_name"]):
            doc = frappe.get_doc({"doctype": "Donor Type", **t})
            doc.insert(ignore_permissions=True)
