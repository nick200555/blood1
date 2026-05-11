# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HealthcareInstitution(Document):
    def update_outstanding(self, amount):
        self.outstanding_balance = (self.outstanding_balance or 0) + amount
        self.save()
