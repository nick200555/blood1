# Copyright (c) 2025, BloodBank Team and contributors

import frappe
from frappe.utils import today, add_days, now_datetime

def auto_update_inventory():
    """Recalculate all inventory records"""
    inventories = frappe.get_all("Blood Inventory")
    for inv in inventories:
        doc = frappe.get_doc("Blood Inventory", inv.name)
        doc.recalculate_stock()
    
    frappe.logger().info("Background Task: Inventory recalculated")

def check_expiry():
    """Identify expired units and mark them"""
    expired_units = frappe.get_all("Blood Unit", filters={
        "status": ["in", ["Quarantined", "Available", "Reserved"]],
        "expiry_date": ["<", today()]
    })
    
    for u in expired_units:
        doc = frappe.get_doc("Blood Unit", u.name)
        doc.status = "Expired"
        doc.save()
        
    if expired_units:
        frappe.logger().info(f"Background Task: {len(expired_units)} units marked as Expired")

def auto_defer_donors():
    """Check for expired deferrals and reactivate donors"""
    deferred = frappe.get_all("Donor", filters={
        "donor_status": "Deferred",
        "deferral_end_date": ["<=", today()],
        "permanent_deferral": 0
    })
    
    for d in deferred:
        doc = frappe.get_doc("Donor", d.name)
        doc.reactivate()
        
    if deferred:
        frappe.logger().info(f"Background Task: {len(deferred)} donors reactivated")

def check_appointment_reminders():
    """Send reminders for tomorrow's appointments"""
    # This is handled by Notification (event: Days Before)
    # But can be extended here for SMS or custom logic
    pass
