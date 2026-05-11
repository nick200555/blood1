# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class BloodInventory(Document):
    def recalculate_stock(self):
        # Count units by status for this branch/group/component
        filters = {
            "current_branch": self.branch,
            "blood_group": self.blood_group,
            "component_type": self.component_type
        }
        
        self.available_units = frappe.db.count("Blood Unit", {**filters, "status": "Available"})
        self.reserved_units = frappe.db.count("Blood Unit", {**filters, "status": "Reserved"})
        self.expired_units = frappe.db.count("Blood Unit", {**filters, "status": "Expired"})
        self.discarded_units = frappe.db.count("Blood Unit", {**filters, "status": "Discarded"})
        self.total_units = self.available_units + self.reserved_units + self.expired_units + self.discarded_units
        
        # Update stock status
        if self.available_units <= (self.critical_stock or 5):
            self.stock_status = "Critical"
        elif self.available_units <= (self.minimum_stock or 10):
            self.stock_status = "Low"
        elif self.available_units >= (self.maximum_stock or 50):
            self.stock_status = "Excess"
        else:
            self.stock_status = "Normal"
            
        self.last_updated = now()
        
        # Update units table (showing only current non-discarded/non-issued units)
        self.set("units_list", [])
        units = frappe.get_all("Blood Unit", 
            filters={**filters, "status": ["in", ["Available", "Reserved", "Quarantined", "Expired"]]},
            fields=["name", "status", "expiry_date", "volume_ml"])
            
        for u in units:
            self.append("units_list", {
                "blood_unit": u.name,
                "status": u.status,
                "expiry_date": u.expiry_date,
                "volume": u.volume_ml
            })
            
        self.save()
