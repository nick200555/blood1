# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Transfusion(Document):
    def on_submit(self):
        # Update patient transfusion history
        if self.patient:
            pat = frappe.get_doc("Patient", self.patient)
            pat.append("transfusion_history", {
                "transfusion": self.name,
                "date": self.transfusion_date,
                "blood_unit": self.blood_unit
            })
            pat.save()
            
        # Create Adverse Reaction if checked
        if self.had_reaction:
            self.create_reaction_record()

    def create_reaction_record(self):
        reaction = frappe.new_doc("Adverse Reaction")
        reaction.transfusion = self.name
        reaction.patient = self.patient
        reaction.blood_unit = self.blood_unit
        reaction.reaction_date = self.transfusion_date
        reaction.insert()
        
        self.reaction_details = reaction.name
        self.db_set("reaction_details", reaction.name)
        
        frappe.msgprint(f"Adverse Reaction record {reaction.name} created for transfusion", alert=True)
