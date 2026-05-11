# BloodBank Management System

Comprehensive Blood Bank Management System built on Frappe Framework and ERPNext v15.

## Features

- **Donor Management**: Registration, Eligibility tracking, Appointments, and Health Screening.
- **Inventory Control**: Blood Unit tracking, Component separation, Expiry management, and Stock analytics.
- **Transactions**: Blood Requests, Issues, Transfusions, and Adverse Reaction tracking.
- **Reporting**: Stock reports, Donor analytics, and Expiry alerts.
- **Automation**: Background tasks for inventory updates and donor reactivation.

## Installation

1.  **Get the app**:
    ```bash
    bench get-app bloodbank https://github.com/nick200555/blood1.git
    ```

2.  **Install the app**:
    ```bash
    bench --site [your-site] install-app bloodbank
    ```

3.  **Migrate**:
    ```bash
    bench --site [your-site] migrate
    ```

## License

MIT
