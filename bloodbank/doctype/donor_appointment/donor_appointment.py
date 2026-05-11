# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class DonorAppointment(Document):
    def validate(self):
        if getdate(self.appointment_date) < getdate(today()) and self.status == "Scheduled":
            frappe.throw("Appointment date cannot be in the past")
            
        # Check if donor is eligible
        donor = frappe.get_doc("Donor", self.donor)
        if not donor.is_eligible:
            frappe.msgprint(f"Warning: Donor {donor.full_name} is currently marked as ineligible. Deferral ends: {donor.deferral_end_date or 'N/A'}", alert=True)
            
        # Check for duplicate appointments on same day
        duplicate = frappe.db.exists("Donor Appointment", {
            "donor": self.donor,
            "appointment_date": self.appointment_date,
            "status": ["not in", ["Cancelled", "No Show"]],
            "name": ["!=", self.name]
        })
        if duplicate:
            frappe.throw(f"Donor already has an appointment on {self.appointment_date}")
