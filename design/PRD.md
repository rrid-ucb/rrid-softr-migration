# Product Requirements Document (PRD)

**Product**: RRID Reviewer Selection System (Frontend Rewrite)
**Status**: Draft
**Target Stack**: Next.js 16, Firebase, Airtable

## 1. Executive Summary

The RRID Reviewer Selection System is a critical tool for managing the peer review workflow of infectious disease preprints. The current Softr-based implementation limits customization and AI integration. This PRD defines the requirements for a ground-up rewrite using Next.js, enabling a more responsive, intelligent, and scalable platform while preserving the existing Airtable backend data structure.

## 2. User Roles & Permissions

| Role | Description | Key Permissions |
| :--- | :--- | :--- |
| **Admin** | System oversight | Full access to all tables, user management, system config. |
| **Assistant Editor (AE)** | Managing assignments | Search reviewers, assign preprints, override AI suggestions. |
| **Student Reviewer** | Conducting reviews | View assigned preprints, claim preprints, submit reviews, track own progress. |
| **Guest/Public** | (If applicable) | Restricted read-only access (likely none, login required). |

## 3. Functional Requirements

### 3.1 Authentication & User Profile
- **FR-01**: Users must log in via Email/Password (Firebase Auth).
- **FR-02**: System must match the logged-in email to the `All Users` table in Airtable base `app6NFX8jCkg5kKxi` to retrieve roles.
- **FR-03**: Users should see a profile summary (Name, Role, "Greenlit" status) in the header/sidebar.

### 3.2 Dashboard (Landing Page)
- **FR-04**: Display a 2x2 grid (or responsive layout) navigation to key modules:
    - Find a Preprint
    - Input Peer Reviewers
    - Quality Checks
    - Progress Review
- **FR-05**: Dashboard should be personalized based on user role (e.g., Students see "My Assignments", AEs see "Queue Status").

### 3.3 Preprint Management
- **FR-06**: **Preprint List View**: Display a sortable, filterable list of preprints from `Preprint Info ONLY` table.
    - **Filters**: Domain (BCS, MedSci, etc.), Status, Assignee.
    - **Search**: Keyword search against Title/Author.
- **FR-07**: **Preprint Detail View**: Show full abstract, authors, links, and current reviewer status.
- **FR-08**: **Claim Functionality**: Allow eligible users (Students) to "Claim" a preprint (Limit: Max 2 active claims).

### 3.4 Reviewer Selection & AI Integration
- **FR-09**: **Propose Reviewer Form**:
    - Fields: Name, Email, Affiliation, Justification.
    - **Logic**: Dynamic requirements (e.g., "Justification" required if email is not institutional).
    - **Validation**: Real-time checks against existing database to prevent duplicates.
- **FR-10**: **AI Suggestions List**:
    - Display AI-generated reviewer candidates for a preprint.
    - Actions: "Evaluate" (Accept), "Reject" (with justification).
- **FR-11**: **Reviewer Evaluation**:
    - Detailed view of a candidate (H-Index, key pubs).
    - Form to Submit "Unable to Evaluate" or "Reject" reasons.

### 3.5 Quality Check Portal
- **FR-12**: Interface for AEs to review student inputs.
- **FR-13**: Ability to "Greenlight" (approve) or "Redlight" (reject) a proposed reviewer.

### 3.6 Dashboards & Analytics
- **FR-14**: **Productivity Dashboard**: Visual charts (using Recharts or similar) showing:
    - Preprints reviewed per week.
    - Team performance metrics.
- **FR-15**: Data must be aggregated from `Team Performance` and `Student Performance` tables.

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-01**: Dashboard load time < 1.5s.
- **NFR-02**: Data updates to Airtable should feel instantaneous (optimistic UI updates) or have clear loading states.

### 4.2 Reliability
- **NFR-03**: Graceful error handling if Airtable API is rate-limited (Exponential backoff).

### 4.3 UI/UX
- **NFR-04**: Mobile-responsive design (critical for students on varying devices).
- **NFR-05**: Accessibility compliance (WCAG 2.1 AA).

## 5. Data Requirements

The system will interact with the following Airtable Bases (as detailed in `design/schema/airtable_schema_report.md`):

1.  **RRID Reviewer Selection Process** (`appAYosfmfSuHWiBT`)
    -   Tables: `Preprint Info ONLY`, `Student Reviewer Inputs`, `Referees`, `Selected`, `Team Performance`.
2.  **RRID_App_User** (`app6NFX8jCkg5kKxi`)
    -   Tables: `Users`, `Preprint Selection User Base`.

## 6. Future Considerations ("Deep Research")

- Architecture must allow for a "Research Agent" tab where an LLM can autonomously browse the web (using Firecrawl/Browserbase) to validate reviewer expertise and surface conflict of interest (COI) data not present in Airtable.

