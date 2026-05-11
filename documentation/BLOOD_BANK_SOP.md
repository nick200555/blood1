# 🩸 BloodBank — Standard Operating Procedure (SOP)
### Enterprise Functional Guide for Blood Bank Operations

---

> **Document Version:** 1.0  
> **Application:** BloodBank on ERPNext v15  
> **Audience:** Blood Bank Managers, Technicians, Receptionists, Doctors, Phlebotomists  
> **Compliance:** WHO / FDA / National Blood Service Standards  

---

## 📋 Table of Contents

1. [Getting Started — System Access](#1-getting-started--system-access)
2. [Module 1 — Donor Management](#2-module-1--donor-management)
3. [Module 2 — Blood Collection & Phlebotomy](#3-module-2--blood-collection--phlebotomy)
4. [Module 3 — Laboratory Testing & Validation](#4-module-3--laboratory-testing--validation)
5. [Module 4 — Component Separation & Processing](#5-module-4--component-separation--processing)
6. [Module 5 — Inventory & Cold Chain Management](#6-module-5--inventory--cold-chain-management)
7. [Module 6 — Blood Requests & Crossmatching](#7-module-6--blood-requests--crossmatching)
8. [Module 7 — Issuance & Transfusion](#8-module-7--issuance--transfusion)
9. [Module 8 — Hemovigilance & Adverse Reactions](#9-module-8--hemovigilance--adverse-reactions)
10. [Module 9 — Mobile Camps & Donation Drives](#10-module-9--mobile-camps--donation-drives)
11. [Daily / Weekly / Monthly Operating Checklist](#11-daily--weekly--monthly-operating-checklist)
12. [User Roles & Responsibility Matrix](#12-user-roles--responsibility-matrix)
13. [Frequently Asked Questions (FAQ)](#13-frequently-asked-questions-faq)
14. [Support & Maintenance](#14-support--maintenance)

---

## 1. Getting Started — System Access

### 1.1 Access the Application

1. Open your browser and go to your BloodBank URL:  
   `https://bloodbank.yourhospital.org`
2. Login with your ERPNext credentials (provided by IT).
3. On the left sidebar, click **Blood Bank** workspace.
4. You will see the **Blood Bank Dashboard** with real-time indicators:
   - 🔴 Critical Stock Levels
   - 🔵 Today's Appointments
   - 🟢 Available Units by Group
   - 🟡 Expiring Units (Next 72 Hours)

---

### 1.2 Initial Setup (One-Time — Admin Only)

> **Who does this:** System Administrator or Blood Bank Manager

| Step | Action | Where |
|---|---|---|
| 1 | Create Blood Bank Branches | Blood Bank → Setup → Blood Bank Branch |
| 2 | Define Donation Sites | Blood Bank → Setup → Donation Site |
| 3 | Configure Blood Groups | Blood Bank → Setup → Blood Group |
| 4 | Seed Master Data | Run `bench execute bloodbank.setup.install.after_install` |
| 5 | Configure Cold Storage Alarms | Blood Bank → Setup → Blood Inventory (Set Thresholds) |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator

Go to **ERPNext → HR → User** and assign each person their role:

| Role | Responsibility |
|---|---|
| Blood Bank Manager | Overall operations, approvals, and reporting |
| Blood Bank Technician | Lab testing, component separation, inventory |
| Blood Bank Receptionist | Donor registration, appointments, requests |
| Blood Donor Coordinator | Camp management, donor recruitment |
| Hemovigilance Officer | Adverse reaction tracking, safety compliance |

---

## 2. Module 1 — Donor Management

> **Purpose:** Manage the donor lifecycle from registration to eligibility tracking, ensuring only safe donors contribute to the blood supply.

---

### 2.1 SOP — Register a New Donor

**Who:** Receptionist / Donor Coordinator  
**When:** First-time donation or registration update  

| Step | Action |
|---|---|
| 1 | Go to **Blood Bank → Donor** |
| 2 | Click **+ New** |
| 3 | Fill in **Full Name**, **Gender**, **Date of Birth**, and **Blood Group** (if known) |
| 4 | Enter **Mobile Number** and **Email** (Crucial for notifications) |
| 5 | Select **Donor Type** (Voluntary / Replacement / Directed) |
| 6 | Upload **ID Proof** and **Photo** |
| 7 | Click **Save** |

✅ **Expected Result:** Donor ID (DN-XXXX) is generated. A welcome notification is sent via email/SMS.

---

### 2.2 SOP — Record Health Screening & Eligibility

**Who:** Lab Technician / Doctor  
**When:** Before every phlebotomy session  

| Step | Action |
|---|---|
| 1 | Go to **Donor Management → Donor Health Screening** |
| 2 | Click **+ New** and select the **Donor** |
| 3 | Record Vitals: **Weight**, **Temperature**, **Pulse**, **BP**, and **Hemoglobin (Hb)** |
| 4 | Complete the **Questionnaire** (Travel history, medications, risk factors) |
| 5 | System auto-checks against **Minimum Standards** (e.g., Weight > 50kg, Hb > 12.5g/dL) |
| 6 | If eligible, set **Eligibility Status** = "Eligible" |
| 7 | If ineligible, select a **Deferral Reason** and set **Deferral End Date** |
| 8 | Click **Save** |

✅ **Expected Result:** If deferred, the Donor status changes to "Deferred" and they are blocked from collections until the deferral period ends.

---

### 2.3 SOP — Schedule a Donor Appointment

**Who:** Receptionist / Donor  
**When:** Booking for a static center or mobile camp  

| Step | Action |
|---|---|
| 1 | Go to **Donor Management → Donor Appointment** |
| 2 | Click **+ New** and select **Donor** |
| 3 | Select **Donation Site** and **Appointment Date/Time** |
| 4 | Set **Appointment Type** (Whole Blood / Platelets / Plasma) |
| 5 | Save |

> **Tip:** Appointment reminders are sent automatically 24 hours before the scheduled time.

---

## 3. Module 2 — Blood Collection & Phlebotomy

> **Purpose:** Safely collect blood from eligible donors and track the primary unit from the moment of collection.

---

### 3.1 SOP — Create a Blood Collection Record

**Who:** Phlebotomist / Technician  
**When:** During the donation process  

| Step | Action |
|---|---|
| 1 | Go to **Blood Collection → + New** |
| 2 | Link the **Donor** and the **Donor Health Screening** (Mandatory) |
| 3 | Enter **Collection Date** and **Time** |
| 4 | Select **Collection Method** (Whole Blood / Apheresis) |
| 5 | Record **Volume Collected (mL)** |
| 6 | Record **Bag Number** and **Collection Site** |
| 7 | Click **Save** and then **Submit** |

✅ **Expected Result:** A new **Blood Unit** (UNIT-XXXX) is automatically created with status "Quarantined". The Donor's donation history is updated.

---

## 4. Module 3 — Laboratory Testing & Validation

> **Purpose:** Perform mandatory infectious disease screening (TTI) and blood grouping to ensure unit safety.

---

### 4.1 SOP — Record Blood Test Results

**Who:** Lab Technician  
**When:** After lab analysis of samples  

| Step | Action |
|---|---|
| 1 | Go to **Testing → Blood Test Result** |
| 2 | Click **+ New** and select the **Blood Unit** |
| 3 | Verify **Blood Group** (ABO/Rh) |
| 4 | Enter results for: **HIV**, **Hepatitis B**, **Hepatitis C**, **Syphilis**, **Malaria** |
| 5 | Select **Result Status** for each (Reactive / Non-Reactive) |
| 6 | System auto-sets **Overall Status** (Pass/Fail) |
| 7 | Click **Save** and then **Submit** |

✅ **Expected Result:** If any TTI is reactive, the Blood Unit is marked for "Discard". If all pass, the unit moves to "Available" or "Processing".

---

## 5. Module 4 — Component Separation & Processing

> **Purpose:** Split whole blood into RBC, Plasma, and Platelets to maximize the utility of a single donation.

---

### 5.1 SOP — Blood Component Separation

**Who:** Lab Technician  
**When:** Within 6–8 hours of collection  

| Step | Action |
|---|---|
| 1 | Go to **Processing → Blood Component** |
| 2 | Click **+ New** and select the **Parent Blood Unit** (Whole Blood) |
| 3 | Add Child Units in the table: **Packed RBC**, **Fresh Frozen Plasma**, **Platelets** |
| 4 | Enter **Volume** and **Expiry Date** for each child component |
| 5 | Set **Separation Method** (Centrifugation) |
| 6 | Save and **Submit** |

✅ **Expected Result:** Parent Whole Blood unit status becomes "Processed". Child units are created and added to "Quarantined" inventory awaiting final release.

---

## 6. Module 5 — Inventory & Cold Chain Management

> **Purpose:** Maintain real-time visibility of stock levels across branches, ensuring FEFO (First-Expired, First-Out).

---

### 6.1 SOP — Monitor Blood Stock

**Who:** Blood Bank Manager / Technician  
**When:** Daily check  

1. Go to **Blood Bank → Workspace**
2. Look at the **Blood Inventory** card.
3. Review the **Stock by Group** chart.
4. Check the **Expiry Alert Report** for units expiring within 3 days.

| Status | Action |
|---|---|
| 🟢 Normal | No action needed. |
| 🟡 Low | Initiate replacement donor recruitment. |
| 🔴 Critical | Notify hospitals, cancel elective surgeries, run urgent donor drive. |

---

## 7. Module 6 — Blood Requests & Crossmatching

> **Purpose:** Manage hospital requests and ensure the right blood reaches the right patient.

---

### 7.1 SOP — Process a Blood Request

**Who:** Receptionist / Technician  
**When:** Hospital/Doctor submits a request  

| Step | Action |
|---|---|
| 1 | Go to **Request & Issue → Blood Request** |
| 2 | Click **+ New** |
| 3 | Select **Healthcare Institution** and **Patient** |
| 4 | Enter **Blood Group** and **Component Type** required |
| 5 | Set **Request Type** (Routine / Urgent / Emergency) |
| 6 | Enter **Units Required** and **Required By** date/time |
| 7 | Save |

✅ **Expected Result:** System checks inventory. If stock exists, technician initiates crossmatching.

---

## 8. Module 7 — Issuance & Transfusion

> **Purpose:** Safely release blood units and track the final outcome for the patient.

---

### 8.1 SOP — Issue Blood Units

**Who:** Blood Bank Technician  
**When:** After successful crossmatch  

| Step | Action |
|---|---|
| 1 | Go to **Request & Issue → Blood Issue** |
| 2 | Click **+ New** and link to the **Blood Request** |
| 3 | Select the specific **Blood Unit(s)** from inventory |
| 4 | Verify **Crossmatch Status** is "Compatible" |
| 5 | Enter **Issued By** and **Person Collecting** |
| 6 | Print the **Issue Note** and attach to the blood bag |
| 7 | Save and **Submit** |

✅ **Expected Result:** Units are removed from Inventory. Status becomes "Issued".

---

## 9. Module 8 — Hemovigilance & Adverse Reactions

> **Purpose:** Track and investigate any negative reactions to blood donation or transfusion.

---

### 9.1 SOP — Record an Adverse Reaction

**Who:** Hemovigilance Officer / Doctor  
**When:** Any reaction reported during or after transfusion  

| Step | Action |
|---|---|
| 1 | Go to **Hemovigilance → Adverse Reaction** |
| 2 | Click **+ New** |
| 3 | Select **Patient** and the **Blood Unit** involved |
| 4 | Select **Reaction Type** (Febrile, Hemolytic, Allergic, TRALI) |
| 5 | Record **Symptoms** and **Severity** |
| 6 | Record **Investigation Results** (Repeat grouping/crossmatch) |
| 7 | Click **Save** |

✅ **Expected Result:** Incident is logged for regulatory reporting. If a systematic error is found, all related units from the same collection are quarantined.

---

## 10. Module 9 — Mobile Camps & Donation Drives

> **Purpose:** Organize and manage off-site donation activities.

---

### 10.1 SOP — Plan a Blood Camp

**Who:** Camp Coordinator  
**When:** Planning phase (Weeks before camp)  

| Step | Action |
|---|---|
| 1 | Go to **Camps → Blood Camp** |
| 2 | Click **+ New** |
| 3 | Set **Venue**, **Start Date**, **End Date**, and **Organizer** |
| 4 | Add **Camp Staff** (Doctors, Nurses, Volunteers) |
| 5 | Create a **Camp Equipment** checklist (Beds, Kits, Coolers) |
| 6 | Save |

---

## 11. Daily / Weekly / Monthly Operating Checklist

### 11.1 Daily (Morning Shift - 30 minutes)

| Task | Who | ERPNext Location |
|---|---|---|
| ☐ Check Temperature Logs of all Fridges | Technician | External / Manual |
| ☐ Review High Priority Blood Requests | Manager | Blood Request List |
| ☐ Mark Expired Units as "Discarded" | Technician | Expiry Alert Report |
| ☐ Sync today's Appointments | Receptionist | Donor Appointment |

---

### 11.2 Weekly (1 hour)

| Task | Who | ERPNext Location |
|---|---|---|
| ☐ Inventory Reconciliation (Physical vs System) | Manager | Blood Inventory |
| ☐ Review Deferred Donors for reactivation | Coordinator | Donor List (Filter: Deferral End Date) |
| ☐ Generate Weekly Collection Summary | Manager | Blood Collection Report |

---

### 11.3 Monthly (3 hours)

| Task | Who | ERPNext Location |
|---|---|---|
| ☐ Analyze Donor Retention Rate | Manager | Donor Analytics |
| ☐ Review Adverse Reaction Statistics | Hemovigilance | Adverse Reaction Report |
| ☐ Institutional Billing Reconciliation | CFO / Manager | Blood Issue Register |

---

## 12. User Roles & Responsibility Matrix

| Feature | Manager | Technician | Receptionist | Coordinator | Hemovigilance |
|---|---|---|---|---|---|
| Donor Registration | 👁 Read | 👁 Read | ✅ Full | ✅ Full | ❌ |
| Health Screening | 👁 Read | ✅ Full | ❌ | ❌ | 👁 Read |
| Blood Collection | 👁 Read | ✅ Full | ❌ | ❌ | ❌ |
| Lab Testing | ✅ Approval | ✅ Full | ❌ | ❌ | ❌ |
| Inventory Edit | ✅ Full | ✅ Full | 👁 Read | ❌ | ❌ |
| Blood Request | 👁 Read | ✅ Process | ✅ Create | ❌ | ❌ |
| Blood Issue | ✅ Approval | ✅ Full | ❌ | ❌ | ❌ |
| Adverse Reactions | ✅ Review | 👁 Read | ❌ | ❌ | ✅ Full |
| Camp Planning | ✅ Approval | ❌ | ❌ | ✅ Full | ❌ |

---

## 13. Frequently Asked Questions (FAQ)

**Q1: A donor has a low Hb (11.0 g/dL). Can I still collect blood?**  
A: No. System validation blocks collection if Hb is below 12.5 g/dL. You must record a "Temporary Deferral" for 30 days and provide iron supplements.

---

**Q2: How do I handle an Emergency Request without a patient blood group?**  
A: Issue **O-Negative** (Universal Donor) Packed RBCs immediately. Create a Blood Request with "Request Type" = **Emergency** and "Blood Group" = **O-**.

---

**Q3: The system shows a unit is expired, but it looks fine. Can I extend the date?**  
A: No. Regulatory compliance strictly prohibits extension of shelf life. The unit MUST be moved to "Discard" status in ERPNext.

---

**Q4: Can a donor donate again after 1 month?**  
A: Not for Whole Blood. Minimum interval is 56 days (8 weeks). The system will block registration of a new collection if the interval is too short.

---

## 14. Support & Maintenance

- **System Issues:** Contact IT Support at `it.support@yourhospital.org`
- **Application Support:** Contact BloodBank Admin at `admin.bloodbank@yourhospital.org`
- **Updates:** System updates are scheduled every Sunday at 02:00 AM.

---
