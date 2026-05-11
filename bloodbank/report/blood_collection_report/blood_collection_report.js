frappe.query_reports["Blood Collection Report"] = {
    "filters": [
        {"fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date"},
        {"fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date"},
        {"fieldname": "branch", "label": __("Branch"), "fieldtype": "Link", "options": "Blood Bank Branch"},
        {"fieldname": "blood_group", "label": __("Blood Group"), "fieldtype": "Link", "options": "Blood Group"},
        {"fieldname": "collection_method", "label": __("Method"), "fieldtype": "Select", "options": "\nWhole Blood\nApheresis-Platelets\nApheresis-Plasma\nApheresis-RBC\nApheresis-Double RBC"}
    ]
};
