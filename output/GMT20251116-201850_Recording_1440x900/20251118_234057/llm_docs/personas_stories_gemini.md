Okay, here is a comprehensive document covering user personas, user stories, feature mapping, and user journeys based on the provided video transcript.

# RRID Reviewer Selection Process - Persona and User Story Document

## 1. User Personas

### 1.1. Editorial Lead (Stef)

*   **Name:** Stef
*   **Role:** Editorial Lead
*   **Background and Context:** Stef is responsible for the overall strategy and quality of the reviewer selection process. She needs to ensure preprints are reviewed efficiently and effectively, and that the right reviewers are selected.
*   **Goals and Motivations:**
    *   Ensure high-quality, timely reviews of preprints.
    *   Optimize reviewer selection to minimize bias and conflict of interest.
    *   Maintain a consistent and well-prioritized workflow for preprint review.
*   **Pain Points and Challenges:**
    *   High volume of preprints to manage.
    *   Ensuring the right preprints are prioritized and sent out.
    *   Keeping track of reviewers to avoid over-inviting or conflicts of interest.
    *   Difficulty in monitoring and improving the performance of the reviewer selection process.
*   **Technical Skill Level:** Intermediate. Comfortable with web applications and data management tools. Needs clear, intuitive interfaces.
*   **How They Would Use This Application:** Stef would use the application to:
    *   Set initial rankings for preprints. (04:14)
    *   Monitor the status of preprints (active, on hold, etc.).
    *   Intervene manually in the reviewer selection process when necessary.
    *   Receive alerts about preprints with high reject rates or low numbers of reviewers. (38:16)
    *   Track and analyze the performance of the reviewer selection process.

### 1.2. Assistant Editor (Angel)

*   **Name:** Angel
*   **Role:** Assistant Editor
*   **Background and Context:** Angel assists with the day-to-day tasks of reviewer selection, including quality checking reviewer suggestions, sending out invites, and monitoring the progress of preprints.
*   **Goals and Motivations:**
    *   Efficiently process preprints and reviewer suggestions.
    *   Ensure quality and accuracy in the reviewer selection process.
    *   Minimize manual effort and errors.
*   **Pain Points and Challenges:**
    *   Time-consuming manual tasks, such as checking for conflicts of interest.
    *   Difficulty in keeping track of reviewer status and invite counts.
    *   Ensuring consistency in reviewer selection criteria.
    *   Having to manually push preprints through workflow.
*   **Technical Skill Level:** Proficient. Comfortable with web applications and data entry. Needs a user-friendly interface that minimizes clicks and errors.
*   **How They Would Use This Application:** Angel would use the application to:
    *   Quality check proposed reviewers. (09:52)
    *   Send out invites to reviewers. (26:44)
    *   Monitor invite counts and preprint status.
    *   Manually send invites when needed. (26:47)
    *   Identify and resolve issues with reviewer suggestions.

### 1.3. Student Reviewer Proposer

*   **Name:** David
*   **Role:** Student Reviewer Proposer
*   **Background and Context:** David is a student contributing to the process by suggesting potential reviewers for preprints.
*   **Goals and Motivations:**
    *   Contribute to scientific community
    *   Gain experience
*   **Pain Points and Challenges:**
    *   Understanding the process to properly write the justification. (10:11)
    *   Following all COI
*   **Technical Skill Level:** Comfortable with data entry.
*   **How They Would Use This Application:** David would use the application to:
    *   Propose potential reviewers for preprints. (05:58)
    *   See when they can select the correct reviewers, and when they have been declined.

### 1.4 AI Model

*   **Name:** Referee AI
*   **Role:** Artificial Intelligence Model
*   **Background and Context:** The AI suggests potential reviewers for preprints.
*   **Goals and Motivations:**
    *   Suggests potential reviewers for preprints. (05:26)
    *   Suggest potential COI (10:59)
*   **Pain Points and Challenges:**
    *   Potential COI.
*   **Technical Skill Level:** Backend.
*   **How They Would Use This Application:** Backend processing

## 2. User Stories

### 2.1. Selected -> Preprint Info (Automations)

*   **As an Editorial Lead,** I want to automatically create a record in Preprint Info when a preprint is selected, so that the preprint is added into the workflow.
*   **Acceptance Criteria:**
    *   When a record is created in "Selected," a corresponding record is created in "Preprint Info Only."
    *   Title and DOI are automatically updated in the "Preprint Info Only" record.
    *   A link is created between the "Selected" record and the "Preprint Info Only" record.
    *   Title and DOI are backed up
    *   Ranking is carried over from editorial and initial
    *   Referees are created.
*   **Priority:** High
*   **Related Pages/Features:** Selected Table, Preprint Info Only Table

### 2.2. Team Performance Tracking

*   **As a System Admin,** I want to automatically track team performance when reviewers are proposed, so that I can monitor team contributions and identify areas for improvement.
*   **Acceptance Criteria:**
    *   When a reviewer is proposed, the system links the proposed reviewer to the team and/or domain.
    *   The team and domain are correctly identified based on the proposer's affiliation (country, domain).
*   **Priority:** Medium
*   **Related Pages/Features:** Preprint Info Only Table, Team Performance Table, Domain Performance Table, Student Reviewer Inputs.

### 2.3. Record Update in SRI (Student Reviewer Inputs)

*   **As a Student Reviewer Proposer,** I want that when I propose a reviewer that it tracks.
*   **Acceptance Criteria:**
    *   When a record is created in "Student Reviewer Inputs," the system links the student proposer to the "All Users" base.
    *   The link to publication is automatically updated.
    *   The proposed reviewer is associated with the relevant preprint.
*   **Priority:** Medium
*   **Related Pages/Features:** Student Reviewer Inputs Table, All Users Table, Preprint Info Only Table

### 2.4. Immediate Reviewer COI Checker

*   **As an Assistant Editor,** I want to check immediately for any COIs when a reviewer is proposed, so that we follow proper protocols
*   **Acceptance Criteria:**
    *   When a record is created in "Student Reviewer Inputs," the system checks for conflicts of interest (author, recent reviewer, duplicate domain).
    *   The system flags any potential conflicts of interest.
*   **Priority:** High
*   **Related Pages/Features:** Student Reviewer Inputs Table

### 2.5. Stef Ranking -> Current Ranking

*   **As an Editorial Lead,** I want that rankings are properly updated, so that I know how to prioritize.
*   **Acceptance Criteria:**
    *   When the "Stef's Ranking" field is updated, the system updates the final ranking of the preprint.
    *   The system adjusts rankings to maintain relative order, taking into account preprints on hold.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table, Selected Table

### 2.6. Rank 0 -> Active (Preprint Workflow)

*   **As an Assistant Editor,** I want to easily make preprints active, so that the preprints continue to move along the workflow.
*   **Acceptance Criteria:**
    *   When the rank is zero or the preprint status is "Active," the system ensures both conditions are true.
    *   The preprint status is set to "In Process."
    *   The "Date In Process" field is updated.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.7. Mini Team 20 -> active

*   **As a Assistant Editor,** I want to get the mini-team incentivized to work on dormant preprints.
*   **Acceptance Criteria:**
    *   When the invite count is >= 20 and the preprint status is "Dormant," the system sets the preprint status to "Active."
*   **Priority:** Medium
*   **Related Pages/Features:** Preprint Info Only Table

### 2.8. Set Preprint Status -> On Hold

*   **As an Editorial Lead,** I want that I know that a preprint is out of invites so it can be properly sent.
*   **Acceptance Criteria:**
    *   When a preprint no longer needs invites, the system sets the preprint status to "On Hold" and "Out of Circulation."
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table, calculation of the amount of invitees needed

### 2.9. Set Preprint Status -> Out of Circulation

*   **As an Assistant Editor,** I want to ensure all preprints have the correct status of out of circulation so the process can move along smoothly.
*   **Acceptance Criteria:**
    *   When quality checking is performed, or invites are done, the preprint can be out of circulation.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.10. Out of Circ -> Back in Queue

*   **As an Assistant Editor,** I want to be able to get back the preprint
*   **Acceptance Criteria:**
    *   When a preprint status is changed from "Out of Circulation" to "More Invites Needed", make it active again
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.11. X Invites -> Check COI

*   **As an Assistant Editor,** I want to be able to ensure there are no COI before sending invites out.
*   **Acceptance Criteria:**
    *   When unsent invites are greater than a number, there are no COIs before an invite is sent out.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.12 Referee Claimed Limit

*   **As an Assistant Editor,** I want to be able to limit students to claim X amount of referees.
*   **Acceptance Criteria:**
    *   When a student claims a referee that it tracks that.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.13 Daily Reject Summary

*   **As an Assistant Editor,** I want to be able to send daily reject summaries.
*   **Acceptance Criteria:**
    *   Send emails of fixable referees.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

### 2.14 Email Student of Fixable Reviewer

*   **As an Assistant Editor,** I want to be able to follow up on fixable referees.
*   **Acceptance Criteria:**
    *   Can send a student the fixable referees.
*   **Priority:** High
*   **Related Pages/Features:** Preprint Info Only Table

## 3. Feature Mapping

| Feature                                    | Persona                | User Need                                                                                               | Justification                                                                                                                                               |
| :----------------------------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selected -> Preprint Info                  | Editorial Lead         | Automate adding preprints to workflow                                                                 | Reduces manual data entry, ensures timely processing                                                                                                     |
| Team Performance Tracking                  | System Admin           | Monitor team contributions and identify areas for improvement                                         | Provides data for performance evaluation, resource allocation                                                                                             |
| Record Update in SRI                        | Assistant Editor       | Link proposers                                                                                                   | Enables comprehensive tracking, improves accountability                                                                                                 |
| Immediate Reviewer COI Checker             | Assistant Editor       | Quickly check for conflicts of interest                                                                 | Minimizes manual effort, reduces the risk of bias                                                                                                         |
| Stef Ranking -> Current Ranking           | Editorial Lead         | Prioritize preprints effectively                                                                      | Ensures high-priority preprints are processed quickly, optimizes resource allocation                                                                     |
| Rank 0 -> Active (Preprint Workflow)       | Assistant Editor       | Simplify activating new preprints                                                                      | Streamlines the workflow, reduces manual steps                                                                                                        |
| Invite Automation                          | Assistant Editor       | Automatically check COI                                                                       | Frees up student for other tasks                                                                                                                               |

## 4. User Journeys

### 4.1. Preprint Enters the System and is Processed

1.  **Entry Point:** A preprint is flagged as "Selected" in the Preprint scraping base. (02:57)
2.  **Action:** The "Selected -> Preprint Info" automation creates a corresponding record in the "Preprint Info Only" table. (03:11)
    *   Title, DOI, and other relevant information are copied to the new record. (03:22)
    *   Initial ranking information (if available) is pulled in. (04:14)
3.  **Action:** A Referee is created (05:26)
4.  **Action:** The "Track Team Performance" automation links the proposed reviewer to the relevant team and domain. (05:50)
5.  **Decision Point:** Stef (Editorial Lead) reviews the preprint and assigns an initial ranking.
    *   If the ranking is high priority (1, 2, 3, 4, 5), the preprint is prioritized for immediate processing. (04:30)
    *   If the ranking is NA, the preprint is set to NA. (04:30)
    *   If the preprint was already out of circulation the change has no effect. (04:43)
6.  **Action:** Angel (Assistant Editor) reviews the proposed reviewers and performs quality checks, including checking for COI. (09:52)
    * The assistant editor looks if the reviewer is the author (10:59)
    * The assistant editor looks for duplicate domains. (11:11)
7.  **Action:** After 20 Invites are reached and no conflicts of interest are found, the invites can be sent out. (23:26)
    *   The system updates the preprint status to "On Hold" and queues it for invites. (24:31)
8.  **Exit Point:** Once the invitations are out, a 3-month time hold will prevent further invites. (32:47)

### 4.2. Quality Checking

1.  **Entry Point:** A preprint has an "Unchecked Count" greater than 10. (37:41)
2.  **Action:** The "Email AE for High Unchecked Daily" automation sends a summary email to assistant editors associated with the relevant domain. (37:54)
3.  **Action:** Angel (Assistant Editor) reviews the reviewers suggested. (37:54)
4. **Decision Point** Is the rejection rate high? If so, notify for a new repopulation.
5.  **Exit Point:** All the reviewers have been reviewed and the "Unchecked Count" is zero. (37:54)

This document provides a solid foundation for understanding user needs and designing a user-centered application.