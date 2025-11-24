# Acceptance Criteria & Test Plan

## 1. Overview
This document defines the criteria for accepting the new Next.js frontend as a replacement for the legacy Softr application. It incorporates requirements from the `PRD`, `SCHEMA`, and insights from the legacy codebase (`rrid-softr-custom-code`).

## 2. Functional Acceptance Criteria

### 2.1 User Authentication & Roles
- [ ] **Login**: User can log in via Firebase Auth (Email/Password).
- [ ] **Role Sync**: System correctly identifies user role (Student, AE, Admin) from Airtable `Users` table upon login.
- [ ] **Redirect**:
    - Students -> Dashboard / My Quality Checks.
    - AEs -> Quality Check Portal.
    - Admins -> Admin Dashboard.

### 2.2 Preprint Management
- [ ] **List View**:
    - Display preprints from `Preprint Info ONLY`.
    - Filter by Domain (BCS, MedSci, PSE, SSH).
    - Search by Title/Author.
    - **Legacy Parity**: Verify "Status" logic matches Softr filters (Active, In Queue).
- [ ] **Detail View**:
    - Show Abstract, DOI link, and Author list.
    - Show "Mini Team" members.

### 2.3 Reviewer Proposal (Complex Form)
*Reference: Legacy `referee_form.js` logic*
- [ ] **Validation**:
    - **Institutional Email**: If email domain is generic (gmail.com, yahoo.com), "Justification" field is **REQUIRED**.
    - **Backup Reviewer**: If "Invite Backup?" is YES, "Backup Name/Email" is **REQUIRED**.
- [ ] **Conflict of Interest (COI) Check**:
    - User clicks "Check COI".
    - System checks against:
        1.  Preprint Authors (fuzzy match name).
        2.  Existing Reviewers in `Student Reviewer Inputs`.
        3.  Recent Referees in `Referees`.
    - **Pass**: Returns "No COI Found".
    - **Warn**: Returns "Potential Author Match" or "Recently Proposed" (does not block, but warns).
- [ ] **Submission**:
    - Successfully creates record in `Student Reviewer Inputs`.
    - Links correctly to `Preprint` record.

### 2.4 AI Suggested Reviewers
- [ ] **Display**: Show list of AI candidates.
- [ ] **Claim Logic**:
    - Student can "Claim" max 2 candidates per preprint.
    - Claiming changes status in local view.
- [ ] **Evaluation**:
    - "Evaluate" button opens detailed view.
    - "Reject" requires selection of Reason Code.

### 2.5 Quality Check (QC) Portal
- [ ] **Queue**: Display proposals with status "Pending QC".
- [ ] **Action**:
    - AE can "Greenlight" (Approve) -> Updates Airtable Status.
    - AE can "Redlight" (Reject) -> Updates Airtable Status.

### 2.6 Dashboards & Gamification
- [ ] **Metrics**:
    - "Greenlit Rate" matches calculation: `(Greenlit / Total Submitted) * 100`.
- [ ] **Badges**:
    - "Novice" badge appears after 1st submission.
    - "Quality Star" badge appears after 5 greenlit reviews.

## 3. Technical Acceptance Criteria

### 3.1 Data Integrity
- [ ] **Schema Validation**: All writes to Airtable must pass Zod schema validation derived from `airtable_complete_schema.json`.
- [ ] **Error Handling**: Graceful degradation if Airtable API returns 429 (Rate Limit).

### 3.2 Performance
- [ ] **Load Time**: Dashboard loads in < 1.5s (LCP).
- [ ] **Search**: Preprint search results return in < 500ms.

## 4. Test Cases (Manual)

| ID | Scenario | Steps | Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | **Institutional Email Check** | 1. Go to Propose Reviewer.<br>2. Enter `test@gmail.com`.<br>3. Try to Submit. | Validation Error: "Justification required for non-institutional email." |
| **TC-02** | **COI Warning** | 1. Go to Propose Reviewer.<br>2. Enter Name = "Existing Author".<br>3. Click Check COI. | Warning: "Potential Conflict: Name matches preprint author." |
| **TC-03** | **Claim Limit** | 1. Claim 2 AI Reviewers.<br>2. Try to Claim 3rd. | Button Disabled or Error Message: "Max claims reached." |
| **TC-04** | **Greenlight Update** | 1. Login as AE.<br>2. Greenlight a proposal.<br>3. Login as Student. | Student Dashboard shows "Greenlit" status increment. |

## 5. Migration Verification
- [ ] **User Mapping**: Verify Firebase UIDs map correctly to 5 sample Airtable User Records.
- [ ] **Data Consistency**: Verify total count of "Active Preprints" in New App == Softr App.

