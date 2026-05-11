# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodGroup(Document):
    def validate(self):
        self.full_group = f"{self.blood_group} {self.rh_factor}"
