frappe.query_reports["Blood Stock Report"] = {
    "filters": [
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Blood Bank Branch"
        },
        {
            "fieldname": "blood_group",
            "label": __("Blood Group"),
            "fieldtype": "Link",
            "options": "Blood Group"
        },
        {
            "fieldname": "component_type",
            "label": __("Component Type"),
            "fieldtype": "Link",
            "options": "Blood Component Type"
        },
        {
            "fieldname": "stock_status",
            "label": __("Stock Status"),
            "fieldtype": "Select",
            "options": "\nNormal\nLow\nCritical\nExcess"
        }
    ]
};
