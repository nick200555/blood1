frappe.query_reports["Blood Issue Register"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "healthcare_institution",
            "label": __("Institution"),
            "fieldtype": "Link",
            "options": "Healthcare Institution"
        },
        {
            "fieldname": "blood_group",
            "label": __("Blood Group"),
            "fieldtype": "Link",
            "options": "Blood Group"
        }
    ]
};
