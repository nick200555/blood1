# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodRequest(Document):
    def on_submit(self):
        self.status = "Submitted"
        self.check_inventory_alert()

    def check_inventory_alert(self):
        # Check if enough stock exists across all branches
        available = frappe.db.sql("""
            SELECT SUM(available_units) 
            FROM `tabBlood Inventory` 
            WHERE blood_group = %s AND component_type = %s
        """, (self.blood_group, self.component_type))[0][0] or 0
        
        if available < self.units_required:
            frappe.msgprint(f"Warning: Only {available} units of {self.blood_group} {self.component_type} are currently available. Request exceeds stock.", alert=True)

    def update_fulfillment(self, units_count, issue_name):
        self.units_fulfilled = (self.units_fulfilled or 0) + units_count
        
        if self.units_fulfilled >= self.units_required:
            self.status = "Fulfilled"
        elif self.units_fulfilled > 0:
            self.status = "Partially Fulfilled"
            
        self.append("fulfillment_details", {
            "blood_issue": issue_name,
            "units_count": units_count,
            "date": frappe.utils.today()
        })
        self.save()
