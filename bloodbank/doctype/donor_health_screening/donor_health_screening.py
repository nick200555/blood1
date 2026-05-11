# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today

class DonorHealthScreening(Document):
    def validate(self):
        # Calculate BMI
        if self.weight_kg and self.height_cm:
            self.bmi = self.weight_kg / ((self.height_cm / 100) ** 2)
            
        # Standard eligibility rules
        if self.weight_kg < 50:
            self.is_eligible = 0
            if not self.deferral_reason:
                self.deferral_reason = frappe.db.get_value("Deferral Reason", {"reason": "Low Weight"}, "name")
                
        if self.hemoglobin_level < 12.5:
            self.is_eligible = 0
            if not self.deferral_reason:
                self.deferral_reason = frappe.db.get_value("Deferral Reason", {"reason": "Low Hemoglobin"}, "name")

    def on_submit(self):
        if not self.is_eligible:
            self.defer_donor()

    def defer_donor(self):
        donor = frappe.get_doc("Donor", self.donor)
        donor.donor_status = "Deferred"
        donor.is_eligible = 0
        donor.deferral_reason = self.deferral_reason
        
        if self.deferral_period_days:
            donor.deferral_end_date = add_days(today(), self.deferral_period_days)
            donor.permanent_deferral = 0
        else:
            # Check if reason is permanent
            reason_type = frappe.db.get_value("Deferral Reason", self.deferral_reason, "deferral_type")
            if reason_type == "Permanent":
                donor.permanent_deferral = 1
        
        donor.save()
        
        # Log to Eligibility Log
        log = frappe.new_doc("Donor Eligibility Log")
        log.donor = self.donor
        log.action = "Deferred"
        log.reason = self.deferral_reason
        log.screening = self.name
        log.deferral_end_date = donor.deferral_end_date
        log.insert()
