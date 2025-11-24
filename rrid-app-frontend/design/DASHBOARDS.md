# Dashboards & Analytics Specification

## 1. Productivity Dashboard
**Target Audience**: Central Team, Assistant Editors (AE).
**Goal**: Track the velocity and quality of the reviewer selection process.

### Data Sources
- **Airtable Tables**: `Team Performance`, `Student Performance`, `Domain Performance`.
- **External**: Prophy (via API or iframe if direct integration unavailable).

### Key Metrics
| Metric | Definition | Source |
| :--- | :--- | :--- |
| **Student Productivity** | Number of reviews submitted/greenlit per week. | `Student Performance` |
| **AE Productivity** | Time to quality check (QC) proposals. | `Team Performance` |
| **Team Pitching** | Number of preprints "pitched" (reviewers proposed) by team. | `Team Performance` |
| **Domain Performance** | Breakdown of activity by scientific domain (BCS, MedSci, etc). | `Domain Performance` |

### Visualizations
- **Charts**: Recharts (Bar/Line) for trends over time.
- **Tables**: Sortable tables for Student/AE rankings.

## 2. Prophy Dashboard
**Purpose**: Integration with Prophy.science to validate reviewer expertise.
**Implementation**: 
- **Phase 1**: Embed existing Prophy interface (iframe).
- **Phase 2**: API integration to pull H-Index and Publication counts directly into the "Reviewer Details" view.

## 3. Invited Preprints
**Purpose**: Operational view for tracking active invitations.
**Columns**:
- Preprint Title (Link)
- Status (Invited, Accepted, Declined)
- Date Invited
- Review Due Date
- Reminders Sent (Count)

## 4. Training & Gamification
**See**: `GAMIFICATION.md`

