# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CampRegistration(Document):
    def on_update(self):
        if self.attended:
            camp = frappe.get_doc("Blood Camp", self.blood_camp)
            camp.update_stats()
