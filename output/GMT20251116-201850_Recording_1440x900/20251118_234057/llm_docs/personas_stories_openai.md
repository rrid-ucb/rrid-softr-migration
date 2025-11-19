# RRID Reviewer Selection Process: Personas and User Stories

## User Personas

### Persona 1: Emily - Student Reviewer
- **Role:** Student Reviewer
- **Background:** Emily is a graduate student in biology, working part-time as a peer reviewer to gain experience in academic publishing.
- **Goals and Motivations:**
  - Gain experience and improve her academic writing and reviewing skills.
  - Contribute to the scientific community.
- **Pain Points and Challenges:**
  - Finding time to review along with her studies.
  - Understanding complex automation processes.
- **Technical Skill Level:** Intermediate
- **How they would use this application:**
  - Emily uses the application to select preprints to review, submit her feedback, and track her reviewing contributions.

### Persona 2: Dr. Smith - Academic Editor
- **Role:** Academic Editor
- **Background:** Dr. Smith is a seasoned academic with years of experience in editing scientific journals.
- **Goals and Motivations:**
  - Ensure the quality and credibility of publications.
  - Mentor young reviewers.
- **Pain Points and Challenges:**
  - Managing multiple submissions and reviewers.
  - Ensuring timely reviews.
- **Technical Skill Level:** Advanced
- **How they would use this application:**
  - Dr. Smith uses the platform to assign reviewers, monitor progress, and ensure preprints are reviewed thoroughly.

### Persona 3: Alex - Automation Specialist
- **Role:** Automation Specialist
- **Background:** Alex is an IT professional focusing on enhancing workflow efficiency through automation.
- **Goals and Motivations:**
  - Improve process efficiency.
  - Reduce manual errors in the reviewing process.
- **Pain Points and Challenges:**
  - Troubleshooting failed automations.
  - Keeping up with updates and changes in the software.
- **Technical Skill Level:** Expert
- **How they would use this application:**
  - Alex uses the platform to develop and maintain automation scripts and ensure smooth execution of processes.

### Persona 4: Mia - Quality Checker
- **Role:** Quality Checker
- **Background:** Mia is responsible for ensuring the review process meets quality standards.
- **Goals and Motivations:**
  - Maintain high quality of reviews.
  - Ensure compliance with review standards.
- **Pain Points and Challenges:**
  - Managing quality checks across numerous submissions.
  - Communicating issues back to reviewers efficiently.
- **Technical Skill Level:** Intermediate
- **How they would use this application:**
  - Mia uses the platform to validate reviews, communicate with reviewers, and track quality metrics.

## User Stories

### Feature: Reviewer Selection
- **User Story for Emily:**
  - As a *Student Reviewer*, I want to *select preprints that match my expertise* so that *I can provide valuable feedback*.
  - **Acceptance Criteria:** Can filter preprints by domain, keyword search enabled, select button visibly available.
  - **Priority:** High
  - **Related Pages/Features:** Preprint Info, Reviewer Selection Page

- **User Story for Dr. Smith:**
  - As an *Academic Editor*, I want to *assign preprints to suitable reviewers* so that *reviews are conducted efficiently*.
  - **Acceptance Criteria:** List of available reviewers, ability to assign, confirmation notification.
  - **Priority:** High
  - **Related Pages/Features:** Reviewer Assignment, Team Performance

### Feature: Automation Management
- **User Story for Alex:**
  - As an *Automation Specialist*, I want to *debug automation scripts* so that *the reviewing process remains uninterrupted*.
  - **Acceptance Criteria:** Error logs available, testing environment prior to deployment.
  - **Priority:** High
  - **Related Pages/Features:** Automations, Scripting Interface

### Feature: Quality Check
- **User Story for Mia:**
  - As a *Quality Checker*, I want to *review completed submissions* so that *all reviews meet quality standards*.
  - **Acceptance Criteria:** Checklist for quality parameters, feedback loop to reviewers.
  - **Priority:** Medium
  - **Related Pages/Features:** QC Portal, Reviewer Feedback

## Feature Mapping

### Major Features and Relevant Personas
1. **Reviewer Selection** - Emily, Dr. Smith
   - **Serves User Needs:** Enables selection and assignment of preprints.
   - **Workflow:** Begins with preprint selection, includes assignment, and ends with review completion.

2. **Automation Management** - Alex
   - **Serves User Needs:** Ensures efficiency and reduces manual workload.
   - **Workflow:** Covers script creation, testing, and deployment stages.

3. **Quality Checking** - Mia
   - **Serves User Needs:** Ensures reviews meet set standards.
   - **Workflow:** Involves submission checks, feedback generation, and compliance reporting.

## User Journeys

### Task: Reviewing a Preprint
- **Entry Point:** Emily logs in and accesses the Preprint Info page.
- **Process:**
  - Filters preprints by domain.
  - Selects a relevant preprint.
  - Enters the review through the Student Reviewer Inputs portal.
- **Exit Point:** Submits review and closes the application.

### Task: Assigning Reviews
- **Entry Point:** Dr. Smith accesses the Reviewer Selection portal.
- **Process:**
  - Lists potential reviewers.
  - Assigns preprints based on expertise and availability.
  - Monitors progress in the Team Performance page.
- **Exit Point:** Once all assignments are confirmed, logs out.

### Task: Managing Automation
- **Entry Point:** Alex accesses the Automations interface.
- **Process:**
  - Reviews recent automation failures.
  - Edits and tests scripts.
  - Deploys updated scripts.
- **Exit Point:** Ensures all automations run successfully and logs out.

## Screenshots and Context

### Context for Specific Screens

- **[Frame at 00:15]:** Introduction to the automation process for reviewer selection. This screen is crucial for understanding initial setup and automation triggers.
- **[Frame at 01:17]:** Displays all users, linking to reviewer performance and productivity metrics.
- **[Frame at 02:17]:** Shows selected preprints ready for the review process.
- **[Frame at 03:26]:** Creation of records in preprint info, important for data accuracy and linkage.
- **[Frame at 04:30]:** Script editor interface for managing reviewer rankings.
- **[Frame at 06:42]:** Tracking team performance and linking proposed reviewers.
- **[Frame at 11:57]:** Automations to update rankings based on new criteria and conditions.
- **[Frame at 18:15]:** Invitation process management, highlighting the importance of the COI check.
- **[Frame at 29:43]:** Approach to completing the review process, ensuring all criteria are fulfilled.

By strategically utilizing these screens and understanding user roles, the application efficiently manages the peer review selection process.