# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, date_diff, getdate, add_days

class Donor(Document):
    def validate(self):
        self.full_name = f"{self.first_name} {self.last_name}".strip()
        if self.date_of_birth:
            self.age = date_diff(getdate(today()), getdate(self.date_of_birth)) // 365
            if self.age < 18 or self.age > 65:
                frappe.msgprint("Warning: Donor age is outside standard range (18-65)", alert=True)

        self.check_eligibility()

    def check_eligibility(self):
        if self.donor_status == "Blacklisted":
            self.is_eligible = 0
            return

        if self.permanent_deferral:
            self.is_eligible = 0
            return

        if self.deferral_end_date and getdate(self.deferral_end_date) > getdate(today()):
            self.is_eligible = 0
            return

        if self.next_eligible_date and getdate(self.next_eligible_date) > getdate(today()):
            self.is_eligible = 0
            return

        self.is_eligible = 1
        self.donor_status = "Active"

    def update_donation_history(self, collection_doc):
        self.last_donation_date = collection_doc.collection_date
        self.total_donations = frappe.db.count("Blood Collection", {"donor": self.name, "docstatus": 1})
        
        # Calculate next eligibility based on donor type interval
        interval = 56 # Default
        if self.donor_type:
            dt = frappe.get_doc("Donor Type", self.donor_type)
            interval = dt.min_donation_interval_days or 56
            
        self.next_eligible_date = add_days(collection_doc.collection_date, interval)
        
        # Append to history table
        self.append("donation_history", {
            "collection": collection_doc.name,
            "date": collection_doc.collection_date,
            "blood_group": collection_doc.blood_group,
            "volume": collection_doc.volume_collected_ml
        })
        self.save()

    def reactivate(self):
        self.donor_status = "Active"
        self.is_eligible = 1
        self.deferral_reason = None
        self.deferral_end_date = None
        self.permanent_deferral = 0
        self.save()
