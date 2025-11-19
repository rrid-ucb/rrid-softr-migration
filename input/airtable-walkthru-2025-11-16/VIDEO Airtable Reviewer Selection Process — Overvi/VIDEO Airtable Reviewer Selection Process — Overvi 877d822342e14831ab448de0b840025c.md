# VIDEO Airtable: Reviewer Selection Process — Overview

Audience: Internal
Category: Airtable
Last Updated: November 16, 2025 1:04 PM
Owner: rrid-dev, Aaron Culich
Status: Draft
Summary: Purpose, key tables, statuses, and workflow for the Reviewer Selection Process Airtable base.
Type: Reference

Base Walk Through

[https://drive.google.com/file/d/1ABO2ol4o_RdAdb7vfrtMBrouwowE9T4-/view?usp=sharing](https://drive.google.com/file/d/1ABO2ol4o_RdAdb7vfrtMBrouwowE9T4-/view?usp=sharing)

# Automation Walkthrough

[Airtable Automations Walkthrough Transcript.txt](VIDEO%20Airtable%20Reviewer%20Selection%20Process%20%E2%80%94%20Overvi/Airtable_Automations_Walkthrough_Transcript.txt)

[https://berkeley.zoom.us/rec/share/GNbAuCSrbJDZTzaj6Bs0IsPePRoPOyPkIuwMF562E8zClwVmoXpfmKpYxxGoyNYI.mizBhq7QTUg74LjX](https://berkeley.zoom.us/rec/share/GNbAuCSrbJDZTzaj6Bs0IsPePRoPOyPkIuwMF562E8zClwVmoXpfmKpYxxGoyNYI.mizBhq7QTUg74LjX)
Passcode: UX4G54Y?

### Purpose

Document how the Reviewer Selection Process base supports selecting and tracking peer reviewers for preprints. Covers table purposes, key fields, statuses, and operational rules.

### Key tables in scope

1. Preprint info only
2. Student reviewer inputs
3. Referees
4. Recent reviewer all users
5. Team performance

### 

### Additional preprint metadata

- Title
- In process (was it made Active)
- Team (used in Team performance tracking)
- Selected date
- Proposer of the preprint
- Authors
- Ideal reviewer profile
- Similar papers
- Gates funding flag

### AI-suggested reviewers interface

- “Updated referees info” feeds AI-suggested reviewers into the Referees base.
- Linkages enable rollups for counts: unclaimed AI reviewers, total generated, reject counts, greenlit count, and overall performance.

### Operational cautions (Views)

- Certain views are consumed by the web app, automations, or are hard-coded. Do not modify or filter these directly.
- When in doubt, create a new view and name clearly. Views labeled “Filter me” are safe to adjust.

### Review cadence

- Keep statuses and counts accurate for downstream automations and reporting.

### Open questions

- Clarify the final distinction between Invited and Complete.
- Confirm any SLAs for moving from Unchecked to QC outcomes.

[https://berkeley.zoom.us/rec/share/GNbAuCSrbJDZTzaj6Bs0IsPePRoPOyPkIuwMF562E8zClwVmoXpfmKpYxxGoyNYI.mizBhq7QTUg74LjX](https://berkeley.zoom.us/rec/share/GNbAuCSrbJDZTzaj6Bs0IsPePRoPOyPkIuwMF562E8zClwVmoXpfmKpYxxGoyNYI.mizBhq7QTUg74LjX)
Passcode: UX4G54Y?