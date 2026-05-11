# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodIssue(Document):
    def on_submit(self):
        units_issued = 0
        for item in self.issued_units:
            # Update blood unit status to Issued
            unit = frappe.get_doc("Blood Unit", item.blood_unit)
            unit.issue_unit(self)
            units_issued += 1
            
        # Update related request fulfillment
        if self.blood_request:
            req = frappe.get_doc("Blood Request", self.blood_request)
            req.update_fulfillment(units_issued, self.name)
            
        # Update healthcare institution balance
        if self.healthcare_institution and self.total_amount:
            inst = frappe.get_doc("Healthcare Institution", self.healthcare_institution)
            inst.update_outstanding(self.total_amount)

    def on_cancel(self):
        # Revert units back to Available
        for item in self.issued_units:
            unit = frappe.get_doc("Blood Unit", item.blood_unit)
            unit.status = "Available"
            unit.notes = f"Issue {self.name} cancelled"
            unit.save()
            
        # Revert healthcare institution balance
        if self.healthcare_institution and self.total_amount:
            inst = frappe.get_doc("Healthcare Institution", self.healthcare_institution)
            inst.update_outstanding(-self.total_amount)
