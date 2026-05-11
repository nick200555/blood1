# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodTestResult(Document):
    def validate(self):
        # Auto-determine overall result
        if (self.hiv_status == "Non-Reactive" and 
            self.hbv_status == "Non-Reactive" and 
            self.hcv_status == "Non-Reactive" and 
            self.syphilis_status == "Non-Reactive" and 
            self.malaria_status == "Negative"):
            self.overall_result = "Passed"
            self.rejection_reason = None
        else:
            self.overall_result = "Failed"
            if not self.rejection_reason:
                self.rejection_reason = "Reactive markers found in mandatory screening"

    def on_submit(self):
        # Update related Blood Units
        units = frappe.get_all("Blood Unit", filters={"blood_collection": self.blood_collection})
        for u in units:
            unit_doc = frappe.get_doc("Blood Unit", u.name)
            
            # Append test result to unit history
            unit_doc.append("test_results", {
                "test": self.name,
                "test_date": self.test_date,
                "result": self.overall_result,
                "tested_by": self.tested_by
            })
            
            if self.overall_result == "Passed":
                unit_doc.status = "Available"
            else:
                unit_doc.status = "Discarded"
                unit_doc.notes = f"Failed tests: {self.rejection_reason}"
            
            unit_doc.save()

        # Update collection status
        collection = frappe.get_doc("Blood Collection", self.blood_collection)
        collection.status = "Tested"
        collection.save()

        # If failed, defer donor
        if self.overall_result == "Failed":
            self.defer_donor()

    def defer_donor(self):
        donor = frappe.get_doc("Donor", self.donor)
        donor.donor_status = "Deferred"
        donor.is_eligible = 0
        donor.permanent_deferral = 1 # Most reactive markers lead to permanent deferral
        donor.deferral_reason = frappe.db.get_value("Deferral Reason", {"reason": "Positive Infectious Marker"}, "name")
        donor.save()
        
        frappe.msgprint(f"Donor {self.donor} has been permanently deferred due to test results", alert=True)
