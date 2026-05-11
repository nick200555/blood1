# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, today

class BloodUnit(Document):
    def validate(self):
        if not self.expiry_date:
            self.set_expiry_date()
        
        if getdate(self.expiry_date) < getdate(today()) and self.status not in ["Issued", "Discarded"]:
            self.status = "Expired"

    def set_expiry_date(self):
        if self.component_type and self.collection_date:
            comp_type = frappe.get_doc("Blood Component Type", self.component_type)
            shelf_life = comp_type.shelf_life_days or 35
            self.expiry_date = add_days(self.collection_date, shelf_life)

    def on_update(self):
        # Trigger inventory update
        self.update_inventory()

    def update_inventory(self):
        # Find or create inventory record for this branch/group/component
        inv_name = frappe.db.get_value("Blood Inventory", 
            {"branch": self.current_branch, "blood_group": self.blood_group, "component_type": self.component_type}, "name")
        
        if inv_name:
            inv = frappe.get_doc("Blood Inventory", inv_name)
            inv.recalculate_stock()
        else:
            inv = frappe.new_doc("Blood Inventory")
            inv.branch = self.current_branch
            inv.blood_group = self.blood_group
            inv.component_type = self.component_type
            inv.insert()
            inv.recalculate_stock()

    def issue_unit(self, issue_doc):
        self.status = "Issued"
        self.notes = f"Issued via {issue_doc.name} on {issue_doc.issue_date}"
        self.save()
