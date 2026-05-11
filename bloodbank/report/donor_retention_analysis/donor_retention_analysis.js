frappe.query_reports["Donor Retention Analysis"] = {
    "filters": [
        {"fieldname": "blood_group", "label": __("Blood Group"), "fieldtype": "Link", "options": "Blood Group"},
        {"fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date"},
        {"fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date"}
    ]
};
