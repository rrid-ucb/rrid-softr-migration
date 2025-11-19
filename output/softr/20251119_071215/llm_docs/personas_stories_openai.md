# Personas and User Stories for Reviewer Selection Application

## 1. User Personas

### Persona 1: Alex the Student Reviewer
- **Role:** Student Reviewer
- **Background:** Undergraduate studying biology, interested in academic publishing.
- **Goals:** Gain experience in peer reviewing, earn badges for achievements.
- **Motivations:** Enhance resume, learn from experts.
- **Pain Points:** Lack of prior experience, finding accessible resources.
- **Technical Skill Level:** Intermediate
- **Usage of Application:** Uses the platform to input peer reviews, track personal progress, and propose reviewers.

### Persona 2: Emily the Assistant Editor
- **Role:** Assistant Editor
- **Background:** Postgraduate with a few years of experience in editing.
- **Goals:** Ensure high-quality reviews are submitted, streamline the review process.
- **Motivations:** Professional growth, improving publication standards.
- **Pain Points:** Coordination with multiple reviewers, managing timelines.
- **Technical Skill Level:** Advanced
- **Usage of Application:** Primarily engages in quality checks, using dashboards for team performance metrics.

### Persona 3: Jordan the Central Team Member
- **Role:** Central Team Member
- **Background:** Experienced editor responsible for overseeing the entire review process.
- **Goals:** Maintain the integrity and efficiency of the review process, implement process improvements.
- **Motivations:** Organizational success, efficient reviewer communication.
- **Pain Points:** Navigation of complex data, preventing process bottlenecks.
- **Technical Skill Level:** Expert
- **Usage of Application:** Uses control panels to manage preprints, update reviewer databases, and manage team workload.

## 2. User Stories

### Landing Page
- **User Story:** As Alex, I want to easily navigate to input peer reviewers so that I can quickly participate in the review process.
  - **Acceptance Criteria:** Navigation links should be clear and visible.
  - **Priority:** High
  - **Related Pages:** Input Peer Reviewers, Progress Review

### Input Peer Reviewers
- **User Story:** As Emily, I want to input peer reviews efficiently so that the quality checks can be processed seamlessly.
  - **Acceptance Criteria:** Forms should be intuitive and provide options for conflict of interest checks.
  - **Priority:** High
  - **Related Pages:** Preprints List, Quality Check Portal

### Quality Check Portal
- **User Story:** As Jordan, I want to access the quality check portal to approve and oversee reviews.
  - **Acceptance Criteria:** Data should be accurately rendered, allowing amendments and approvals.
  - **Priority:** High
  - **Related Pages:** My Quality Checks, Preprint Control Panel

### Productivity Dashboard
- **User Story:** As Alex, I want to see my progress and achievements so that I can monitor improvement and earn badges.
  - **Acceptance Criteria:** Display of badges and achievements must be up-to-date.
  - **Priority:** Medium
  - **Related Pages:** Achievement and Training Dashboard

### Achievement and Training Dashboard
- **User Story:** As Emily, I want to track team badges and achievements to understand overall team capability.
  - **Acceptance Criteria:** Accurate tracking of team productivity and training results.
  - **Priority:** Medium
  - **Related Pages:** Productivity Dashboard

## 3. Feature Mapping

### Input Peer Reviewers
- **Relevant Personas:** Alex, Emily
- **User Needs:** Enable easy submission and conflict check of potential reviewers.
- **Workflow:** Navigate from the landing page to preprints, propose reviewers using forms, submit to database.

### Quality Check Portal
- **Relevant Personas:** Emily, Jordan
- **User Needs:** Support in reviewing proposed reviewers, managing conflicts.
- **Workflow:** Access quality check listings, use automation and scripts for conflict resolution, approve or reject reviewers.

### Achievement and Training Dashboard
- **Relevant Personas:** Alex, Emily
- **User Needs:** Visual presentation of reviewer engagement and success.
- **Workflow:** Display earned badges, track training progress, report achievements.

## 4. User Journeys

### Journey: Proposing a Reviewer
- **Start:** Alex Logs in -> Navigates to "Input Peer Reviewers"
- **Middle:** Fills the form -> Conducts Conflict Check
- **End:** Submits Reviewer -> Receives Confirmation
- **Branches:** If conflict arises, notify the user with feedback.

### Journey: Managing Quality Checks
- **Start:** Emily Opens Quality Check Portal
- **Middle:** Reviews listing with Data from Airtable -> Marks reviews for final checks
- **End:** Approves, Rejects, or Requests more information
- **Branches:** Adjustments made as new conflicts are identified by scripts and algorithms.

## 5. Screenshots and Context

### Frame at 00:00
- **Context:** Overview of key features on the landing page. Guides users to key actions like finding a preprint or inputting peer reviewers.

### Frame at 01:06
- **Context:** Shows navigation to the preprints list, indicating a separation between active preprints and those in queue for better workflow management.

### Frame at 04:13
- **Context:** Displays the propose a reviewer page, including forms and conflict resolution checks, crucial for Alex’s user journey.

### Frame at 13:32
- **Context:** Depicts the quality check portal where Emily and Jordan can manage the reviewing process and quality standards.

### Frame at 17:38
- **Context:** Features the productivity dashboard enabling users to track personal and team productivity metrics.

These frames provide visual anchors to support and streamline user stories and journeys within the application.