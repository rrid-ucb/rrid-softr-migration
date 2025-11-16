# Personas and User Stories for Preprint Review Software

## User Personas

### Persona 1: Emma – Student Reviewer
- **Name and Role:** Emma, Student Reviewer
- **Background and Context:** A graduate student in biology with an interest in scientific publishing.
- **Goals and Motivations:** Wants to gain experience in peer review to enhance her CV and learn more about the publishing process.
- **Pain Points and Challenges:** Unsure about the review process and struggles with understanding the workflow.
- **Technical Skill Level:** Intermediate user familiar with academic platforms but new to this application.
- **How they would use this application:** Emma uses the platform to propose reviewers and track their progress in the process.

### Persona 2: Alex – Assistant Editor
- **Name and Role:** Alex, Assistant Editor
- **Background and Context:** A postdoc researcher who recently took the role of an assistant editor.
- **Goals and Motivations:** Aim to ensure quality reviews are conducted efficiently and preprints are processed without delay.
- **Pain Points and Challenges:** Managing multiple reviews and ensuring each receives enough attention is challenging.
- **Technical Skill Level:** Advanced user, comfortable with database systems and platform navigation.
- **How they would use this application:** Uses the system to manage reviewer assignments, check quality, and track review progress.

### Persona 3: Sarah – Central Team Member
- **Name and Role:** Sarah, Central Team Member
- **Background and Context:** Experienced editor responsible for overseeing multiple review processes.
- **Goals and Motivations:** Wants to ensure smooth operation across all reviews and enhance productivity.
- **Pain Points and Challenges:** Handling workflow bottlenecks and ensuring consistency across reviews.
- **Technical Skill Level:** Expert user who manages database integration and custom scripts.
- **How they would use this application:** Primarily uses administrative interfaces to adjust settings and manage the overview of review processes.

## User Stories

### Landing Page
- **User Story:** As a Student Reviewer, I want to view my dashboard so that I can see my review tasks.
  - **Acceptance Criteria:** The dashboard shows pending reviews and task details.
  - **Priority:** High
  - **Related pages/features:** Dashboard, Review Tasks

### Preprint List Page
- **User Story:** As an Assistant Editor, I want to access the preprint list so that I can assign reviewers to new submissions.
  - **Acceptance Criteria:** Display a list of preprints and their statuses.
  - **Priority:** High
  - **Related pages/features:** Preprint Details, Assign Reviewers

### Article Details and Add Reviewers
- **User Story:** As a Central Team Member, I want to review the details of a preprint so that I can ensure all necessary information is present.
  - **Acceptance Criteria:** Display preprint metadata including authors and affiliations.
  - **Priority:** Medium
  - **Related pages/features:** Review Proposal Form, COI Check

### Quality Check Portal
- **User Story:** As an Assistant Editor, I want to perform a quality check on review proposals so that I can approve or reject them.
  - **Acceptance Criteria:** Highlight invalid proposals or COI issues.
  - **Priority:** High
  - **Related pages/features:** Reviewer Evaluation

### Productivity Dashboard
- **User Story:** As a Central Team Member, I want to track productivity metrics so that I can identify areas for performance improvement.
  - **Acceptance Criteria:** Show summaries of student and editorial activities.
  - **Priority:** Medium
  - **Related pages/features:** Achievements and Training Dashboard

## Feature Mapping

### Find a Preprint
- **Relevant Personas:** Emma, Alex
- **Serves User Needs:** Helps in identifying submissions that require attention and input.
- **Workflows:** Links to preprint detail pages where further actions can be taken.

### COI Check and Proposed Reviewer Form
- **Relevant Personas:** Emma, Alex
- **Serves User Needs:** Ensures transparency and avoids conflicts in the review process.
- **Workflows:** Span COI checks and approval processes.

### Achievement and Training Dashboard
- **Relevant Personas:** Emma, Sarah
- **Serves User Needs:** Tracks learning progress and motivates students through badge earnings.
- **Workflows:** Includes personal accomplishments and learning modules.

## User Journeys

### Reviewer Proposal Submission
1. **Entry Point:** Dashboard
2. **Path:** Access preprint page -> Check details -> Submit reviewer proposals via form
3. **Exit Point:** Confirmation of submission
4. **Decision Points:** Verification of conflict of interest, proposal approval

### Quality Checking
1. **Entry Point:** Landing Page -> Quality Check Portal
2. **Path:** Load reviews needing quality checks -> Validate or reject proposals
3. **Exit Point:** Status update confirmation
4. **Decision Points:** Reject or approve proposals based on criteria

## Screenshots and Context

### Landing Page
- **Timestamps:** [00:47], [01:06]
- **Description:** Displays dashboard with insights into ongoing preprints and tasks.

### Preprint List and Details
- **Timestamps:** [02:14], [05:04]
- **Description:** Shows active and queued preprints, links to details and actions.

### Quality Check Portal
- **Timestamps:** [13:38], [13:52]
- **Description:** Portal where proposals undergo quality checks, decision-making interface.

### Achievement and Training Dashboard
- **Timestamps:** [19:59], [20:28]
- **Description:** Displays badges and accomplishments for motivation and tracking.

## Additional Details

### Header Navigation
- **Timestamps:** [21:37]
- **Description:** Provides fast access to main sections like dashboard, proposals, and settings.
