frappe.query_reports["Expiry Alert Report"] = {
    "filters": [
        {"fieldname": "days_to_expiry", "label": __("Days to Expiry"), "fieldtype": "Int", "default": 7},
        {"fieldname": "branch", "label": __("Branch"), "fieldtype": "Link", "options": "Blood Bank Branch"},
        {"fieldname": "blood_group", "label": __("Blood Group"), "fieldtype": "Link", "options": "Blood Group"}
    ]
};
