# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodComponent(Document):
    def on_submit(self):
        # Create a new Blood Unit for the separated component
        self.create_component_unit()

    def create_component_unit(self):
        # Fetch parent collection details
        collection = frappe.get_doc("Blood Collection", self.blood_collection)
        
        unit = frappe.new_doc("Blood Unit")
        unit.blood_collection = self.blood_collection
        unit.donor = self.donor
        unit.blood_group = self.blood_group
        unit.collection_date = collection.collection_date
        unit.component_type = self.component_type
        unit.volume_ml = self.volume_ml
        unit.blood_bag_number = f"{self.parent_unit}-{self.component_id}"
        unit.current_branch = collection.branch
        unit.status = "Quarantined" # Still needs to inherit parent test status or be re-tested
        unit.insert()
        
        self.new_unit_created = unit.name
        self.db_set("new_unit_created", unit.name)
        
        frappe.msgprint(f"Component Unit {unit.name} created")
