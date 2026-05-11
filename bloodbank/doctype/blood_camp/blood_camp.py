# Copyright (c) 2025, BloodBank Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BloodCamp(Document):
    def update_stats(self):
        # Update actual donor count and volume from collections linked to this site (if camp is a site)
        # Assuming the camp name is used in donation_site or linked via Camp Registration
        self.actual_donors = frappe.db.count("Camp Registration", {"blood_camp": self.name, "attended": 1})
        self.save()
