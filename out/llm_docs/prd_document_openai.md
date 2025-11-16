# Product Requirements Document (PRD)

## Executive Summary

This document outlines the requirements for rebuilding the reviewed software application, as illustrated in a video walkthrough. The software is designed to facilitate a peer review process for scientific preprints, providing distinct user roles with tailored interfaces and functionalities. The following documentation details each screen, its components, functionalities, and interactions necessary for developers to recreate the application's UI and logic.

## Table of Contents

1. [Landing Page](#landing-page)
2. [Preprints List Page](#preprints-list-page)
3. [Article Details and Add Reviewers Page](#article-details-and-add-reviewers-page)
4. [Propose a Reviewer Form](#propose-a-reviewer-form)
5. [Evaluate Suggested Reviewer Page](#evaluate-suggested-reviewer-page)
6. [Quality Check Portal](#quality-check-portal)
7. [Preprint Control Panel](#preprint-control-panel)
8. [Productivity Dashboard](#productivity-dashboard)
9. [Achievement and Training Dashboard](#achievement-and-training-dashboard)

---

## 1. Landing Page

### Purpose

To provide the users with an entry point, displaying options based on their roles—students and assistant editors.

### URL/Navigation Path

- Not explicitly mentioned in the video.

### Visual Layout Description

- Header with navigation options
- Two main views toggle: Students View and Assistant Editors View

### UI Components

- Two views selector (Students, Assistant Editors)

### Features and Functionality

- Display of available options based on user role
- Redirection to specific functionalities like proposing reviewers or quality checking

### Data Displayed

- User role-driven content

### User Interactions Available

- Selecting user role
- Navigating to specific functions through view toggles

### Business Logic and Rules

- Various functionalities are role-dependent

### Edge Cases or Validation Mentioned

- Not discussed

## 2. Preprints List Page

### Purpose

Displays the list of preprints and allows users to add reviewers or view preprints.

### URL/Navigation Path

- Links to different sections like "Preprints List"
  
### Visual Layout Description

- List of preprints, categorized into "Active Preprints" and "Preprints in Queue"

### UI Components

- Preprints listing
- "Add Reviewers" button
- Filters and conditional displays

### Features and Functionality

- Display of all preprints accessible to users
- Role-based permissions for adding reviewers

### Data Displayed

- List of preprints and their current status

### User Interactions Available

- Adding reviewers
- Viewing specific preprints

### Business Logic and Rules

- Role restrictions on adding reviewers
- Priority and visibility determined by the user role

### Edge Cases or Validation Mentioned

- Not all preprints have "Add Reviewers" buttons for students

## 3. Article Details and Add Reviewers Page

### Purpose

To display specific details of a selected preprint and facilitate adding reviewers.

### URL/Navigation Path

- Preprint details are accessed via preprint ID in URL

### Visual Layout Description

- Detailed view of a preprint including metadata and AI-suggested reviewers.

### UI Components

- Fields like title, authors, affiliations
- Reviewers list
- "Add Reviewer" interface

### Features and Functionality

- Display of preprint details
- Options to manage reviewer lists
- Integration with external data sources for metadata

### Data Displayed

- Preprint metadata
- AI-suggested reviewers

### User Interactions Available

- Reviewing preprint details
- Adding or managing reviewers

### Business Logic and Rules

- Reviewer additions are validated against conflicts of interest

### Edge Cases or Validation Mentioned

- Preformat changes impact parsing

## 4. Propose a Reviewer Form

### Purpose

For adding new reviewers while checking for conflicts of interest.

### URL/Navigation Path

- Accessed via the "Add Reviewers" action

### Visual Layout Description

- Form fields for inputting reviewer information
- Conflict of interest checks

### UI Components

- Input fields: First Name, Last Name, Email
- Conflict of Interest (COI) checker

### Features and Functionality

- Checking for COI
- Form submission

### Data Displayed

- Input data and COI feedback

### User Interactions Available

- Entering reviewer details
- COI validation

### Business Logic and Rules

- Validation to prevent adding authors as reviewers
- Scripts embedded for COI checking

### Edge Cases or Validation Mentioned

- Validation feedback before proceeding

## 5. Evaluate Suggested Reviewer Page

### Purpose

To evaluate the suitability of AI-suggested reviewers.

### URL/Navigation Path

- Reached via "Evaluate" action on suggested reviewers

### Visual Layout Description

- Reviewer details displayed with evaluation options

### UI Components

- Reviewer information
- Evaluation options: Unable to Evaluate, Reject, Propose

### Features and Functionality

- Evaluate AI-suggested reviewers
- Display pertinent reviewer information

### Data Displayed

- Reviewer profile and associated metadata

### User Interactions Available

- Reviewing and evaluating AI suggestions

### Business Logic and Rules

- Coding fixes for proposing verified suggestions

### Edge Cases or Validation Mentioned

- Automation checks overlapping with existing reviewers

## 6. Quality Check Portal

### Purpose

To allow review and quality checking by assistant editors and central team.

### URL/Navigation Path

- Internal URL for assistant editors and central team

### Visual Layout Description

- List view with proposed reviewers for quality checks

### UI Components

- Reviewer list with statuses
- Filters for in-process and complete preprints

### Features and Functionality

- Reviewer quality checks
- Status updates on reviews

### Data Displayed

- Review details with progress features

### User Interactions Available

- Quality checking workflows

### Business Logic and Rules

- Access restricted to central team

### Edge Cases or Validation Mentioned

- Rendering issues noted in certain conditions

## 7. Preprint Control Panel

### Purpose

To manage preprint visibility and status by the central team.

### URL/Navigation Path

- Admin-specific access, not public

### Visual Layout Description

- Control options for preprint information management

### UI Components

- Management controls for preprint activation and ranking

### Features and Functionality

- Edit preprint status and details

### Data Displayed

- Summary information and actions on preprints

### User Interactions Available

- Editing and managing preprint visibility

### Business Logic and Rules

- Central team exclusive controls

### Edge Cases or Validation Mentioned

- Update functions sometimes non-functional

## 8. Productivity Dashboard

### Purpose

To track productivity metrics of students and editorial teams.

### URL/Navigation Path

- Specific path for productivity tracking

### Visual Layout Description

- Dashboard view with multiple metrics

### UI Components

- Productivity metrics and domain performance indicators
- Custom code embeds

### Features and Functionality

- Visualization of productivity metrics
- Performance tracking for central and assistant editors

### Data Displayed

- Metrics of various users and domains

### User Interactions Available

- Interact with embedded productivity metrics

### Business Logic and Rules

- Embeds for data visualization

### Edge Cases or Validation Mentioned

- Outdated information indicated in demos

## 9. Achievement and Training Dashboard

### Purpose

Tracks user achievements and provides ongoing training feedback.

### URL/Navigation Path

- Base linked to air table

### Visual Layout Description

- Badge and progress tracking interface

### UI Components

- Badges for milestones, progress indicators

### Features and Functionality

- Badge award system
- Progress monitoring for user training

### Data Displayed

- Badge acquisition and user training progress

### User Interactions Available

- Monitoring and inspiring user engagement

### Business Logic and Rules

- Encouragement through gamification elements

### Edge Cases or Validation Mentioned

- Missing progress notations

---

## Technical Requirements

- The application must interface with Airtable for data management.
- Custom scripts are embedded for dynamic interactions.
- User role-specific access control to dictate UI/functional accessibility.

## User Interactions and Workflows

- The focus is on intuitive user flows based on user roles.
- Real-time data rendering and validation to ensure input integrity.
- Seamlessly toggle across various views and paths, fitting the predefined user role paths.

## Data Models Implied by the UI

- User profiles with roles (students, assistant editors, central team)
- Preprints with associated metadata and status fields
- Reviewer profiles and evaluator records

Please refer to the screenshots at given timestamps in the video transcript for visual layout guidance.