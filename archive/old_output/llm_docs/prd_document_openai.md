# Product Requirements Document (PRD) for the Software Application

## Executive Summary

This document provides a detailed product requirements specification for rebuilding the software application demonstrated in a video walkthrough. The goal is to capture the essential pages, functionalities, and design elements of the application to guide the development of a new version from scratch. This document outlines the distinct pages, user interactions, business logic, and data models implied by the UI, ensuring a comprehensive understanding of the existing application structure.

## Table of Contents

1. [Landing Page](#landing-page)
2. [Preprints List](#preprints-list)
3. [Article Details and Add Reviewers](#article-details-and-add-reviewers)
4. [Propose a Reviewer Form](#propose-a-reviewer-form)
5. [Quality Check Portal](#quality-check-portal)
6. [Preprint Control Panel](#preprint-control-panel)
7. [Productivity Dashboard](#productivity-dashboard)
8. [Achievement and Training Dashboard](#achievement-and-training-dashboard)
9. [Technical Requirements](#technical-requirements)
10. [User Interactions and Workflows](#user-interactions-and-workflows)
11. [Data Models Implied by the UI](#data-models-implied-by-the-ui)

## 1. Landing Page

**Purpose:**  
The landing page serves as the entry point for the software, providing navigation to different user roles and functionalities.

**URL/Navigation Path:** Not explicitly mentioned.

**Visual Layout:**
- Two main views: one for students and another for assistant editors.

**UI Components:**
- Navigation menus
- Links to student and assistant editor views

**Features and Functionality:**
- Differentiated views based on user role
- Access to different functionalities: proposed reviewers list, quality checks, etc.

**Data Displayed:**
- User role-specific options

**User Interactions:**
- Navigation to other pages based on user role

**Business Logic:**
- Role-based content filtering

## 2. Preprints List

**Purpose:**  
Displays a list of preprints with options to add peer reviewers and manage entries.

**URL/Navigation Path:** Preprint List Page

**Visual Layout:**
- List of preprints with buttons for managing peer reviewers
- Conditional filters

**UI Components:**
- Preprint listings
- "Add Reviewers" buttons
- Filters for visibility and selection

**Features and Functionality:**
- Separate active preprints, preprints in queue, and prioritized preprints
- Visibility options for students and assistant editors

**Data Displayed:**
- Preprint details including title, status, and review buttons

**User Interactions:**
- Filter and view preprints
- Add reviewers for assistant editors

**Business Logic:**
- Role-based permissions for adding reviewers

**Edge Cases/Validation:**
- Restrict button access based on user role

## 3. Article Details and Add Reviewers

**Purpose:**  
Display detailed information about a specific preprint and allow the addition of reviewers.

**URL/Navigation Path:** /article-details/{preprint-ID}

**Visual Layout:**
- Preprint information details
- Add reviewers functionality

**UI Components:**
- Title, DUI, authors, affiliation details
- AI-suggested reviewers list

**Features and Functionality:**
- Show preprint details and related articles
- Display ideal reviewer profile
- Manage reviewer suggestions

**Data Displayed:**
- Preprint ID, related articles, reviewer list

**User Interactions:**
- Add or remove reviewers

**Business Logic:**
- Preprint-specific data fetching
- Validation for reviewer additions

**Edge Cases/Validation:**
- Check for conflicts of interest

## 4. Propose a Reviewer Form

**Purpose:**  
Facilitates proposing a peer reviewer for a preprint.

**URL/Navigation Path:** /propose-reviewer

**Visual Layout:**
- Form to propose reviewers

**UI Components:**
- Input fields for reviewer details (name, email, etc.)
- Submit button

**Features and Functionality:**
- Conflict of interest check
- Validation for existing reviewers

**Data Displayed:**
- Input fields pre-populated based on existing data

**User Interactions:**
- Form submission
- Real-time feedback on conflict matches

**Business Logic:**
- Validation against existing records
- Conflict of interest detection

**Edge Cases/Validation:**
- Prevent duplicate entries

## 5. Quality Check Portal

**Purpose:**  
Centralized portal for managing proposed reviewers' quality checks.

**URL/Navigation Path:** /quality-check

**Visual Layout:**
- List of proposed reviewers for quality checks
- Simple text instructions

**UI Components:**
- Table of proposed reviewers
- Filter options

**Features and Functionality:**
- Display in-progress and completed quality checks
- Manage reviewer evaluations

**Data Displayed:**
- List and status of reviews

**User Interactions:**
- Filter and manage reviewers

**Business Logic:**
- Quality check based on user role

## 6. Preprint Control Panel

**Purpose:**  
Allows central team to manage preprint information and statuses.

**URL/Navigation Path:** Not explicitly mentioned.

**Visual Layout:**
- Controls for preprint status and information

**UI Components:**
- Buttons and fields for status updates

**Features and Functionality:**
- Activate preprints
- Update ranking and email information

**Data Displayed:**
- Preprint fields and status

**User Interactions:**
- Update preprint information

**Business Logic:**
- Restricted access for central team only

## 7. Productivity Dashboard

**Purpose:**  
Displays productivity metrics related to student and team activities.

**URL/Navigation Path:** Not explicitly mentioned.

**Visual Layout:**
- Embedded Airtable views and metrics

**UI Components:**
- Visual charts and tables

**Features and Functionality:**
- Show individual and team productivity
- Drill down into specific areas

**Data Displayed:**
- Productivity metrics and statistics

**User Interactions:**
- Navigate through productivity insights

**Business Logic:**
- Metric calculations and thresholds

## 8. Achievement and Training Dashboard

**Purpose:**  
Tracks achievements and training progress for users.

**URL/Navigation Path:** Not explicitly mentioned.

**Visual Layout:**
- Training status and badges display

**UI Components:**
- Progress bars, badges, tabs

**Features and Functionality:**
- Track badges earned and training progression

**Data Displayed:**
- Badge and training status

**User Interactions:**
- View and track progress

**Business Logic:**
- Progression logic for learning tracks

## 9. Technical Requirements

- Integration with Airtable for data management
- Custom scripts for data fetching and validation
- Responsive design for multiple user roles

## 10. User Interactions and Workflows

- Role-based navigation and page views
- Form submissions with real-time validation
- Access control for specific functionalities

## 11. Data Models Implied by the UI

- User roles and permissions data
- Preprint metadata and status tracking
- Reviewer suggestions and evaluation data

---

This PRD, based on the video walkthrough, provides a comprehensive guide to the existing application structure. It is intended for developers to rebuild the application with all essential features and functionalities accurately.