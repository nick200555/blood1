# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodCollection(Document):
    def on_submit(self):
        # Create a Blood Unit upon submission
        self.create_blood_unit()
        
        # Update donor record
        donor = frappe.get_doc("Donor", self.donor)
        donor.update_donation_history(self)
        
        # Update appointment status
        if self.appointment:
            apt = frappe.get_doc("Donor Appointment", self.appointment)
            apt.status = "Completed"
            apt.save()

    def create_blood_unit(self):
        unit = frappe.new_doc("Blood Unit")
        unit.blood_collection = self.name
        unit.donor = self.donor
        unit.blood_group = self.blood_group
        unit.collection_date = self.collection_date
        unit.volume_ml = self.volume_collected_ml
        unit.blood_bag_number = self.blood_bag_number
        unit.current_branch = self.branch
        unit.status = "Quarantined"
        
        # Determine component type (default to Whole Blood if not specified)
        unit.component_type = "Whole Blood" 
        unit.insert()
        
        frappe.msgprint(f"Blood Unit {unit.name} created and marked as Quarantined")

    def on_cancel(self):
        # Mark related blood units as discarded
        units = frappe.get_all("Blood Unit", filters={"blood_collection": self.name})
        for u in units:
            unit_doc = frappe.get_doc("Blood Unit", u.name)
            unit_doc.status = "Discarded"
            unit_doc.notes = f"Cancelled due to Collection {self.name} cancellation"
            unit_doc.save()
