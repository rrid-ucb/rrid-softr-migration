# Product Requirements Document: RID Reviewer Selection Platform

**Version:** 1.0
**Date:** October 26, 2023
**Author:** Gemini

## Executive Summary

This document outlines the requirements for rebuilding the RID (Rapid Infectious Diseases) Reviewer Selection Platform. The platform, currently implemented using Softr and Airtable, aims to streamline the process of identifying, proposing, and evaluating peer reviewers for preprints. The platform caters to different user roles including students, assistant editors, and the central team, each with specific permissions and functionalities.  This PRD details each page visible in the video walkthrough, including UI elements, functionality, and data flows. The goal is to provide a comprehensive blueprint for developers to recreate the platform from scratch, enabling improved scalability, maintainability, and future enhancements.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Goals](#goals)
3.  [Target Audience](#target-audience)
4.  [Scope](#scope)
5.  [Functional Requirements](#functional-requirements)
    *   [Landing Page](#landing-page)
    *   [Preprints List](#preprints-list)
    *   [Article Details + Add Reviewer](#article-details--add-reviewer)
        *   [Check for COI](#check-for-coi)
        *   [Propose a Reviewer](#propose-a-reviewer)
        *   [List of AI Suggested Reviewers](#list-of-ai-suggested-reviewers)
    *   [Referee Details](#referee-details)
        *   [Reject Reviewer](#reject-reviewer)
        *   [Propose Reviewer](#propose-reviewer-referee-details)
    *   [Quality Check Portal](#quality-check-portal)
        *   [Status Flags](#status-flags)
        *   [In Process Preprints](#in-process-preprints)
    *   [Quality Check Portal - Vinaj](#quality-check-portal---vinaj) (Likely Test Environment)
    *   [Quality Check Portal - Rishab](#quality-check-portal---rishab) (Likely Test Environment)
    *   [Quality Check Portal Complete](#quality-check-portal-complete)
    *   [My Quality Checks](#my-quality-checks)
    *   [Preprint Control Panel](#preprint-control-panel)
    *   [User Database](#user-database)
    *   [Prophy Dashboard](#prophy-dashboard)
    *   [Invited Preprints](#invited-preprints)
    *   [Help](#help)
    *   [Productivity Dashboard](#productivity-dashboard)
    *   [Central Student Performance](#central-student-performance)
    *   [Training Preprint Proposals](#training-preprint-proposals)
    *   [Achievement and Training Dashboard](#achievement-and-training-dashboard)
    *   [Training Roster](#training-roster)
    *   [Training Referee Proposals Details](#training-referee-proposals-details)
    *   [Training Proposals](#training-proposals)
    *   [Training Quality Checks](#training-quality-checks)
    *   [Student - My Productivity](#student---my-productivity)
    *   [Header Navigation](#header-navigation)
6.  [Non-Functional Requirements](#non-functional-requirements)
7.  [Data Model](#data-model)
8.  [Technical Requirements](#technical-requirements)
9.  [Future Considerations](#future-considerations)

## 1. Introduction

This document provides detailed specifications for the RID Reviewer Selection Platform.  It serves as a comprehensive guide for the development team to build a robust, user-friendly, and scalable application. The document covers the application's purpose, features, functionality, user roles, data model, and technical requirements.

## 2. Goals

*   Rebuild the existing RID Reviewer Selection Platform with improved performance and scalability.
*   Provide a more maintainable and extensible codebase.
*   Improve the user experience for all user roles.
*   Centralize data management and reporting.
*   Retain all existing functionality while laying the groundwork for future enhancements.

## 3. Target Audience

*   Students: Propose peer reviewers for preprints.
*   Assistant Editors: Quality check proposed reviewers, propose reviewers for specific preprints.
*   Central Team: Manage preprints, user data, and overall platform performance.

## 4. Scope

This PRD covers the functional and non-functional requirements for the core features of the RID Reviewer Selection Platform as presented in the video walkthrough. This includes the user interface, data management, business logic, and user roles. It does *not* include functionality that is not directly visible or described in the video.

## 5. Functional Requirements

### Landing Page

*   **Page Name:** Landing Page
*   **Purpose:** Serves as the entry point for users, directing them to different platform features based on their role and needs.
*   **URL/Navigation Path:** `/` (Assumed to be the root URL)
*   **Visual Layout Description:**  [Frame at 00:00] & [Frame at 00:40]  The page is structured with a series of feature blocks arranged in a grid layout.
*   **UI Components:**
    *   **Logo:** Top left corner.
    *   **Feature Blocks (4 visible, presumably more below):**
        *   "Find a Preprint": Browse and pitch infectious disease preprints.  Button: "Go to Preprints". Links to external site.
        *   "Input Peer Reviewers": Select peer reviewers for preprints.  No button visible in the example, but expected to link to the Preprint List page.
        *   "Quality Checks": View the list of your proposed reviewers. No button visible in the example, but expected to link to the Quality Check Portal.
        *   "Progress Review": Track your personal performance. No button visible in the example, but expected to link to a personal dashboard.
*   **Features and Functionality:**
    *   Directs users to relevant platform features based on their role.
    *   Provides a high-level overview of platform capabilities.
*   **Data Displayed:** Titles, descriptions, and potentially images within each feature block.
*   **User Interactions Available:** Clicking on feature blocks to navigate to different platform sections.
*   **Business Logic and Rules:**  The visibility of certain feature blocks may be role-based. Students might not see the same options as Assistant Editors or the Central Team. The "Find a Preprint" links to a separate site for pitching preprints.  The other blocks likely link to internal pages.

### Preprints List

*   **Page Name:** Preprints List
*   **Purpose:** Displays a list of preprints, categorized by different criteria (e.g., active, in queue, prioritized, spotlight). Allows users to select preprints for reviewer proposals.
*   **URL/Navigation Path:** `/preprint-list` (Inferred from [02:27])

![Screenshot at 02:27](../frames/frame_00019_02-27.jpg)

*   **Visual Layout Description:**  [Frame at 02:05] & [Frame at 02:42] The page is structured as a list of preprints, likely displayed in a table or card format. The list is dynamically filtered based on several criteria.
*   **UI Components:**
    *   **Search Bar:**  Allows users to search for specific preprints (visible in "Preprints in Queue" section [02:42]).

![Screenshot at 02:42](../frames/frame_00021_02-42.jpg)

    *   **Filters/Tabs:**  Allows users to filter the list based on domain, rank, preprint status, etc.
    *   **Preprint Cards/Table Rows:** Each entry displays information about a preprint.
        *   Domain
        *   Rank (visible in "Preprints in Queue" section [02:42]).

![Screenshot at 02:42](../frames/frame_00021_02-42.jpg)

        *   DOI (Likely)
        *   Reviewer Discipline
        *   Reviewer Method Expertise
        *   Reviewer Topical Expertise
        *   Corresponding Author Email
        *   Invite Count
        *   Unchecked Count
        *   Assignee
    *   **"Add Reviewers" Button:**  For each preprint, navigates to the Article Details + Add Reviewer page.
*   **Features and Functionality:**
    *   Displays a filtered list of preprints based on different categories.
    *   Allows users to search for specific preprints.
    *   Provides access to preprint details and the reviewer proposal process.
    *   Different sections of the page are conditionally displayed based on user role and preprint status.
*   **Data Displayed:** Preprint metadata including title, DOI, authors, affiliations, and reviewer-related information.
*   **User Interactions Available:**
    *   Searching for preprints using the search bar.
    *   Filtering the list using the available filters.
    *   Clicking the "Add Reviewers" button to propose reviewers for a specific preprint.
*   **Business Logic and Rules:**
    *   **Conditional Visibility:** Different sections of the page are visible based on user role and preprint status:
        *   **Active Preprints List:** Visible to all users (students, assistant editors). [02:50]

![Screenshot at 02:50](../frames/frame_00022_02-50.jpg)

        *   **Preprints in Queue:** Assistant editors can "Add Reviewers," students cannot. [03:04]

![Screenshot at 03:04](../frames/frame_00024_03-04.jpg)

        *   **Prioritized Selected Preprint:** Visible to members of the "mini team" for that preprint. [03:31]

![Screenshot at 03:31](../frames/frame_00028_03-31.jpg)

            *   Conditional filter: email is within the many team emails [03:42]

![Screenshot at 03:42](../frames/frame_00029_03-42.jpg)

            *   Conditional filter: Does not actually need any invites [04:00]

![Screenshot at 04:00](../frames/frame_00031_04-00.jpg)

            *   Conditional filter: Is not active yet [04:00]

![Screenshot at 04:00](../frames/frame_00031_04-00.jpg)

        *   **Two Pitch Editorials:** Students who are part of a "mini team" can propose up to 10 reviewers. [04:08]

![Screenshot at 04:08](../frames/frame_00032_04-08.jpg)

        *   **Assistant Editor Preprint Spotlight:** Visible only to assistant editors. [04:19]  These are preprints with one review, or close to the required number of reviews.

![Screenshot at 04:19](../frames/frame_00034_04-19.jpg)

    *   The "Add Reviewers" button navigates to the Article Details + Add Reviewer page, passing the preprint ID in the URL.

### Article Details + Add Reviewer

*   **Page Name:** Article Details + Add Reviewer
*   **Purpose:** Displays detailed information about a specific preprint and allows users to propose reviewers for that preprint.
*   **URL/Navigation Path:** `/article-details?preprintId={preprintId}` (Inferred from [05:24]) - The preprint ID is passed as a query parameter.

![Screenshot at 05:24](../frames/frame_00042_05-24.jpg)

*   **Visual Layout Description:** [Frame at 05:14] The page presents detailed information about a preprint, including metadata, related articles, and tools for proposing reviewers.
*   **UI Components:**
    *   **Preprint Details Block:** Displays information about the preprint.
        *   Title
        *   DOI
        *   Authors
        *   Affiliations
        *   Similar Articles
        *   Ideal Reviewer Profile
        *   Related Works
    *   **Mini Team List:**  Displays the members of the "mini team" associated with the preprint. Includes functionality to add/remove members (although presenter notes it wasn't true in preview mode) [05:54]

![Screenshot at 05:54](../frames/frame_00046_05-54.jpg)

        *   Add/Remove Team Members button.
    *   **List of AI Suggested Reviewers:** Displays a list of reviewers suggested by an AI algorithm. Claimed reviewers are also visible.
    *   **"Check for COI" section:**  A form to check for Conflict of Interest.
        *   First Name field
        *   Last Name field
        *   Reviewer Email field
        *   "Check COI" button.
    *   **"Propose a Reviewer" form:**  A form to submit a new reviewer proposal.
*   **Features and Functionality:**
    *   Displays comprehensive information about a specific preprint.
    *   Provides a mechanism to add or remove "mini team" members.
    *   Integrates AI-suggested reviewers.
    *   Allows users to check for conflicts of interest before proposing a reviewer.
    *   Provides a form to propose new reviewers.
*   **Data Displayed:**
    *   Preprint metadata (title, DOI, authors, affiliations, etc.).
    *   "Mini team" member data (names, emails, etc.).
    *   AI-suggested reviewer data (name, affiliation, relevant publications, etc.).
*   **User Interactions Available:**
    *   Adding/removing members to the "mini team."
    *   Claiming and evaluating AI-suggested reviewers.
    *   Entering reviewer information into the "Check for COI" form.
    *   Submitting the "Propose a Reviewer" form.
*   **Business Logic and Rules:**
    *   The page dynamically filters the data based on the preprint ID passed in the URL.
    *   Custom code is used to validate the "Propose a Reviewer" form and prevent duplicate proposals. [07:52]

![Screenshot at 07:52](../frames/frame_00061_07-52.jpg)

    *   Data is pulled from Airtable using custom scripts.
    *   The "parsing algorithm" extracts info to generate the AI suggested reviewers, so changes in the format can break the system [06:14]

![Screenshot at 06:14](../frames/frame_00049_06-14.jpg)

    *   Basic input only COI [06:41]

![Screenshot at 06:41](../frames/frame_00052_06-41.jpg)

*   **Edge Cases or Validation Mentioned:**
    *   The AI-suggested reviewer parsing algorithm can fail if the data format changes. [06:14]

![Screenshot at 06:14](../frames/frame_00049_06-14.jpg)

    *   The "Add/Remove Team Members" functionality may not work correctly in preview mode. [05:54]

![Screenshot at 05:54](../frames/frame_00046_05-54.jpg)

    *   Custom code checks for existing authors, reviewers, and proposed reviewers before allowing a user to submit the "Propose a Reviewer" form. [07:15 - 09:31]
        *   The process of checking to see if it's an author or proposed reviewer is "hacky and not reliable." [08:50]

![Screenshot at 08:50](../frames/frame_00067_08-50.jpg)

        *   Provides live feedback to the user that it found a match. [09:16]

![Screenshot at 09:16](../frames/frame_00070_09-16.jpg)

        *   Stops the person from being able to continue [09:22]

![Screenshot at 09:22](../frames/frame_00071_09-22.jpg)


#### Check for COI

*   **Purpose:** To allow users to check for potential conflicts of interest with a proposed reviewer prior to officially proposing them.
*   **UI Components:**
    *   First Name Field (text input)
    *   Last Name Field (text input)
    *   Reviewer Email Field (email input)
    *   Check COI Button
    *   COI Results Table (Displays results of the COI check)
        *   Name
        *   COI Status
        *   Status (Reject, etc)
*   **Features and Functionality:**
    *   Takes in the name and email address of a proposed reviewer.
    *   Submits that information to a COI check.
    *   Displays the results of the COI check in a table format.
*   **Data Displayed:**
    *   COI status of a proposed reviewer (e.g. "COI Status" column)
*   **User Interactions Available:**
    *   Entering the proposed reviewer's first name, last name, and email.
    *   Clicking the "Check COI" button to initiate the COI check.
    *   Reviewing the results of the COI check in the table.
*   **Business Logic and Rules:**
    *   The process is configured as "Basic input only" [06:41]

![Screenshot at 06:41](../frames/frame_00052_06-41.jpg)

    *   The data is not saved into the Quality Check portal as it's only a check [06:41]

![Screenshot at 06:41](../frames/frame_00052_06-41.jpg)

    *   The check runs every 15 minutes [06:34]

![Screenshot at 06:34](../frames/frame_00051_06-34.jpg)


#### Propose a Reviewer

*   **Purpose:** To collect all the information required to propose a reviewer for a Preprint.
*   **UI Components:**
    *   Reviewer First Name (text input)
    *   Reviewer Last Name (text input)
    *   Reviewer Email (email input)
    *   Justification if not Institutional Email (text input/textarea)
    *   Affiliation (text input)
    *   Invite Backup? (boolean)
    *   Invite Backup For... (text input/textarea)
    *   Justify if you think the reviewer should not be the backup (text input/textarea)
    *   Affiliation Conflict of Interest (text input/textarea)
    *   Justification for Affiliation Conflict of Interest (text input/textarea)
    *   Submit Button
*   **Features and Functionality:**
    *   Gathers all information for proposing a reviewer.
*   **Data Displayed:** None (this is an input form)
*   **User Interactions Available:**
    *   Entering information into the fields.
    *   Submitting the form.
*   **Business Logic and Rules:**
    *   Submitting the form sends data to Airtable.

#### List of AI Suggested Reviewers

*   **Purpose:** To list AI suggested reviewers, and provide options for users to claim or reject them.
*   **UI Components:**
    *   Actions (Evaluate button)
    *   Name
    *   Status (Claimed)
    *   Pubmed
    *   Student Email Claimed
    *   Author Url
*   **Features and Functionality:**
    *   Users can claim AI suggested reviewers.
    *   Users can evaluate them.
    *   After claiming two AI suggested reviewers, subsequent AI suggested reviewers will show as "unable to evaluate."
*   **Data Displayed:** Data relating to each AI suggested reviewer.
*   **User Interactions Available:**
    *   Clicking the Evaluate button [10:02]

![Screenshot at 10:02](../frames/frame_00076_10-02.jpg)

*   **Business Logic and Rules:**
    *   Claimed status is tracked.
    *   Users can only claim two AI suggested reviewers before they become "unable to evaluate."

### Referee Details

*   **Page Name:** Referees details
*   **Purpose:** This page appears to show the details of a referee/reviewer.
*   **URL/Navigation Path:** Appears to be opened as a URL when "Evaluate" is clicked on the "List of AI Suggested Reviewers" on the "Article Details + Add Reviewer" page. This URL includes pre-filled data in Airtable [11:12]

![Screenshot at 11:12](../frames/frame_00085_11-12.jpg)

*   **Visual Layout Description:** [Frame at 11:21] Displays details of a reviewer.
*   **UI Components:**
    *   Helmut Burgmann (Name)
    *   Email
    *   Author URL
    *   ORCID
    *   Student Email Claimed
    *   Status (Reject)
    *   HI-index
    *   Unable to Evaluate Button
    *   Reject Reviewer form
        *   Justification for Student Reject
        *   Submit Button
    *   Propose Reviewer Form
*   **Features and Functionality:**
    *   Shows a proposed reviewer's details.
    *   Has the ability to Reject a reviewer.
    *   Has the ability to Propose a reviewer.
*   **Data Displayed:** Details of the proposed reviewer.
*   **User Interactions Available:**
    *   Pressing the Unable to Evaluate button.
    *   Submitting the Reject Reviewer form.
    *   Submitting the Propose Reviewer form.
*   **Business Logic and Rules:**
    *   Clicking evaluate will come to this page and see reviewers details provided by Profi. [11:38]

![Screenshot at 11:38](../frames/frame_00088_11-38.jpg)

    *   If not enough information, the user can click "unable to evaluate" [11:53]

![Screenshot at 11:53](../frames/frame_00090_11-53.jpg)

    *   Custom code is present on the Propose Reviewer form to ensure the student isn't adding someone already proposed or a recent reviewer [12:40]

![Screenshot at 12:40](../frames/frame_00098_12-40.jpg)


#### Reject Reviewer

*   **Purpose:**  Allows users to reject the currently viewed reviewer and provide justification.
*   **UI Components:**
    *   Justification for Student Reject (text area)
    *   Submit Button
*   **Features and Functionality:**
    *   Allows users to reject a proposed reviewer.
*   **Data Displayed:** N/A
*   **User Interactions Available:**
    *   Entering a justification.
    *   Submitting the rejection.
*   **Business Logic and Rules:**
    *   Rejection goes to the student reviewer inputs table. [12:21]

![Screenshot at 12:21](../frames/frame_00095_12-21.jpg)

    *   Referees table leaves the referee table. [12:21]

![Screenshot at 12:21](../frames/frame_00095_12-21.jpg)

    *   Already be flagged as student reject [12:21]

![Screenshot at 12:21](../frames/frame_00095_12-21.jpg)

    *   This is a way for assistant editors to see who's getting rejected by Profi [12:25]

![Screenshot at 12:25](../frames/frame_00096_12-25.jpg)


#### Propose Reviewer (Referee Details)

*   **Purpose:**  Proposes a reviewer.
*   **UI Components:**
    *   Reviewer Email (text input)
    *   Justification if not Institutional Email (text area)
    *   Affiliation (text input)
    *   Backup Reviewer (boolean)
    *   Invite backup for? (text area)
    *   Justify if you think the reviewer shouldn't be the backup (text area)
    *   Affiliation Conflict of Interest (text area)
    *   Justification for affiliation conflict of interest (text area)
    *   Submit button
*   **Features and Functionality:**
    *   Proposes a reviewer.
*   **Data Displayed:** N/A
*   **User Interactions Available:**
    *   Interacting with the form.
    *   Submitting the form.
*   **Business Logic and Rules:**
    *   Custom code present on the Propose Reviewer form to ensure the student isn't adding someone already proposed or a recent reviewer [12:40]

![Screenshot at 12:40](../frames/frame_00098_12-40.jpg)

    *   There is automation to make sure that AI suggested reviewers that have been recently invited are cancelled or hidden. [13:05]

![Screenshot at 13:05](../frames/frame_00101_13-05.jpg)


### Quality Check Portal

*   **Page Name:** Quality Check Portal
*   **Purpose:**  Allows assistant editors and the central team to review proposed reviewers.
*   **URL/Navigation Path:** `/quality-check-portal` (Likely, inferred)
*   **Visual Layout Description:** [Frame at 13:38] & [Frame at 14:14]  A page containing a status explanation, and several lists of preprints by status.
*   **UI Components:**
    *   Status explanation.
    *   Filters (Domain, Preprint Status).
    *   Preprint listings.
*   **Features and Functionality:**
    *   Review proposed reviewers.
*   **Data Displayed:** Preprint domain, and status.
*   **User Interactions Available:**
    *   Filtering preprints.
*   **Business Logic and Rules:**
    *   Only for in process preprints, ones that are not yet complete [15:01]

![Screenshot at 15:01](../frames/frame_00117_15-01.jpg)


#### Status Flags

*   **Purpose:** To explain the status flags.
*   **UI Components:**
    *   On Hold status [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   In Queue status [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   Invited for Other Preprint status [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   Duplicate Email Domain flag [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   Should Not Be Invite Backup flag [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   Extremely Low H-Index flag [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

    *   Low H-Index flag [13:38]

![Screenshot at 13:38](../frames/frame_00106_13-38.jpg)

*   **Features and Functionality:**
    *   Explains the meaning of the status flags.
*   **Data Displayed:** Text explanations of each status.
*   **User Interactions Available:** None
*   **Business Logic and Rules:**
    *   The HTML is being rendered directly in the Softr page [14:37]

![Screenshot at 14:37](../frames/frame_00114_14-37.jpg)


#### In Process Preprints

*   **Purpose:** To allow assistant editors and the central team to review preprints currently in process.
*   **UI Components:**
    *   Preprint team
    *   Domain
    *   Preprint Status (Active, On Hold, In Queue)
*   **Features and Functionality:**
    *   Shows in process preprints.
*   **Data Displayed:** Data about the preprints.
*   **User Interactions Available:** N/A
*   **Business Logic and Rules:**
    *   This custom code is rendering the data using its own scripts [14:46]

![Screenshot at 14:46](../frames/frame_00115_14-46.jpg)


### Quality Check Portal - Vinaj
### Quality Check Portal - Rishab

*   **Notes:** These pages are identified as testers [13:44], and are likely test/development environments for the Quality Check Portal.

![Screenshot at 13:44](../frames/frame_00107_13-44.jpg)


### Quality Check Portal Complete

*   **Purpose:** Quality check portal for completed reviews [15:01]

![Screenshot at 15:01](../frames/frame_00117_15-01.jpg)


### My Quality Checks

*   **Purpose:** A student's view of the Quality Check Portal.
*   **Visual Layout Description:** Similar layout to the Quality Check Portal [15:16]

![Screenshot at 15:16](../frames/frame_00119_15-16.jpg)

*   **Features and Functionality:**
    *   Student can see the outcome of their proposed reviewers.
*   **Data Displayed:** In process and complete reviews.
*   **Business Logic and Rules:**
    *   Student can't see other people's proposed reviewers [15:26]

![Screenshot at 15:26](../frames/frame_00120_15-26.jpg)

    *   Filtered for the student that is logged in [15:34]

![Screenshot at 15:34](../frames/frame_00121_15-34.jpg)


### Preprint Control Panel

*   **Purpose:** Provides a way for the central team to manage preprints and their information without logging into Airtable.
*   **Features and Functionality:**
    *   Central team can make a preprint active [16:15]

![Screenshot at 16:15](../frames/frame_00126_16-15.jpg)

    *   Central team can update a preprint's ranking [16:15]

![Screenshot at 16:15](../frames/frame_00126_16-15.jpg)

    *   Central team can improve preprint information [16:23]

![Screenshot at 16:23](../frames/frame_00127_16-23.jpg)

*   **Business Logic and Rules:**
    *   Only visible to central team [15:56]

![Screenshot at 15:56](../frames/frame_00123_15-56.jpg)

    *   Can only edit fields and actions that are enabled [16:28]

![Screenshot at 16:28](../frames/frame_00128_16-28.jpg)

    *   Can update Maintain email and reviewer profile information [16:36]

![Screenshot at 16:36](../frames/frame_00129_16-36.jpg)

    *   Provides a way for central team to change user information without logging into Airtable directly [16:46]

![Screenshot at 16:46](../frames/frame_00131_16-46.jpg)


### User Database

*   **Purpose:** Provides a way for the central team to manage user information without logging into Airtable.
*   **Features and Functionality:**
    *   Can set a person to active [17:00]

![Screenshot at 17:00](../frames/frame_00132_17-00.jpg)

    *   Choose the number of units, team, or domain, or how they're participating. [17:24]

![Screenshot at 17:24](../frames/frame_00135_17-24.jpg)

*   **Business Logic and Rules:**
    *   For central team to go in and update information about the user database.

### Prophy Dashboard

*   **Purpose:** To see how prophy is doing.
*   **Visual Layout Description:** Embedded airtable interfaces [17:38]

![Screenshot at 17:38](../frames/frame_00137_17-38.jpg)

*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Invited Preprints

*   **Purpose:** To track reviews that are sent out [17:55]

![Screenshot at 17:55](../frames/frame_00139_17-55.jpg)

*   **Features and Functionality:**
    *   To come in and update those reviews that are sent out [18:02]

![Screenshot at 18:02](../frames/frame_00140_18-02.jpg)

    *   Automate the finding of reviewers to receiving those reviews. [17:47]

![Screenshot at 17:47](../frames/frame_00138_17-47.jpg)

*   **Data Displayed:**
    *   Preprint title, doi, preprint status, rank, reviewer outreach status, reviews received, accepts.

### Help

*   **Purpose:** Provides intro things for people to have access to [18:23]

![Screenshot at 18:23](../frames/frame_00143_18-23.jpg)

*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A
*   **Notes:** Outdated content.

### Productivity Dashboard

*   **Purpose:** Provides a dashboard for central and assistant editors to see productivity metrics [18:40]

![Screenshot at 18:40](../frames/frame_00145_18-40.jpg)

*   **Visual Layout Description:** Embedded Airtable interfaces.
*   **UI Components:**
    *   Tabs for:
        *   Student Productivity [18:47]

![Screenshot at 18:47](../frames/frame_00146_18-47.jpg)

        *   AE Productivity
        *   Team Performance
        *   Domain Performance
        *   Search Students
        *   Team Pitching
        *   Overview
        *   Team Performance
        *   Domain Performance
        *   Complete Preprints
*   **Features and Functionality:**
    *   Track student productivity
    *   Track AE productivity
    *   Track team performance
    *   Track domain performance
    *   Search for students
    *   Track team pitching
*   **Business Logic and Rules:**
    *   All custom code [19:06]

![Screenshot at 19:06](../frames/frame_00149_19-06.jpg)

    *   All air table embeds [19:18]

![Screenshot at 19:18](../frames/frame_00150_19-18.jpg)

    *   Interface or an actual view being embedded [19:27]

![Screenshot at 19:27](../frames/frame_00151_19-27.jpg)


### Central Student Performance

*   **Purpose:** Central's view of the student performance dashboard
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A
*   **Notes:** Might be outdated [19:33]

![Screenshot at 19:33](../frames/frame_00152_19-33.jpg)


### Training Preprint Proposals

*   **Purpose:** Unknown, unlabeled tab.
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Achievement and Training Dashboard

*   **Purpose:** Onboard and train users, provide them with information on badges [19:52]

![Screenshot at 19:52](../frames/frame_00154_19-52.jpg)

*   **Visual Layout Description:** Connected to it's own base within AirTable.
*   **UI Components:**
    *   Tabs for:
        *   My Overview [20:09]

![Screenshot at 20:09](../frames/frame_00156_20-09.jpg)

        *   RRID Essentials
        *   Peer Reviewer Selection [20:21]

![Screenshot at 20:21](../frames/frame_00158_20-21.jpg)

        *   Preprint Pitching
        *   Visualizations
        *   Rousseline Gomez (user's name)
        *   Benvay (domain)
        *   Reviewer (role)
        *   Units
        *   Total # Greenlit
        *   Total # Reject
        *   Expected Greenlit Achieved
        *   Preprints Selected
        *   Editorial Pitched Cumulative
        *   Total Preprints Claimed
        *   Team Pitched Cumulative
        *   Update Profile Button
*   **Features and Functionality:**
    *   Allows users to track what they've been able to succeed in managing. [20:53]

![Screenshot at 20:53](../frames/frame_00162_20-53.jpg)

*   **Data Displayed:** User progress, badges, statistics.
*   **Business Logic and Rules:**
    *   Connected to its own base within air table called, I think, training dashboard, something like that [19:52]

![Screenshot at 19:52](../frames/frame_00154_19-52.jpg)


### Training Roster

*   **Purpose:** Likely a roster of those training
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Training Referee Proposals Details

*   **Purpose:** Likely the training information of a referee's proposals.
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Training Proposals

*   **Purpose:** Training for proposals
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Training Quality Checks

*   **Purpose:** Training for quality checks.
*   **Features and Functionality:** N/A
*   **Data Displayed:** N/A

### Student - My Productivity

*   **Purpose:** To allow a student to get direct feedback [21:10]

![Screenshot at 21:10](../frames/frame_00163_21-10.jpg)

*   **Visual Layout Description:** Similar layout to the Achievement and Training dashboard
*   **Features and Functionality:**
    *   How many people have I? [21:10]

![Screenshot at 21:10](../frames/frame_00163_21-10.jpg)

    *   What's my total green light rate? [21:21]

![Screenshot at 21:21](../frames/frame_00164_21-21.jpg)

*   **Data Displayed:**
    *   Total green light rate
*   **Business Logic and Rules:**
    *   important numbers that they know that they need to be tracking to be able to pass [21:26]

![Screenshot at 21:26](../frames/frame_00165_21-26.jpg)


### Header Navigation

*   **Purpose:** Provides navigation throughout the application.
*   **UI Components:**
    *   Landing Page (link)
    *   Propose Reviewers (link)
    *   QC Portal (link)
    *   My Quality Checks (link)
    *   Dashboards (link)
    *   Administration (link)
*   **Business Logic and Rules:**
    *   The visibility of header navigation options is determined by user role [21:36]

![Screenshot at 21:36](../frames/frame_00166_21-36.jpg)


## 6. Non-Functional Requirements

*   **Performance:** The platform should be responsive and load quickly, even with large datasets.
*   **Scalability:** The platform should be able to handle a growing number of users and preprints.
*   **Security:** The platform should protect sensitive user data and prevent unauthorized access.
*   **Accessibility:** The platform should be accessible to users with disabilities.
*   **Maintainability:** The codebase should be well-organized and easy to maintain.

## 7. Data Model

Based on the UI and functionality described in the video, the following data models can be inferred:

*   **User:**
    *   UserID (Primary Key)
    *   FirstName
    *   LastName
    *   Email
    *   Role (Student, Assistant Editor, Central Team)
    *   Team
    *   Domain
    *   Units
    *   Active (boolean)
*   **Preprint:**
    *   PreprintID (Primary Key)
    *   Title
    *   DOI
    *   Abstract
    *   Authors (List)
    *   Affiliations (List)
    *   ReviewerDiscipline
    *   ReviewerMethodExpertise
    *   ReviewerTopicalExpertise
    *   CorrespondingAuthorEmail
    *   InviteCount
    *   UncheckedCount
    *   Assignee
    *   Status (Active, In Queue, On Hold, Complete)
    *   Ranking
    *   NeedsInvites (boolean)
*   **Reviewer:**
    *   ReviewerID (Primary Key)
    *   FirstName
    *   LastName
    *   Email
    *   Affiliation
    *   ORCID
    *   AuthorURL
    *   StudentEmailClaimed
    *   HIIndex
*   **ReviewerProposal:**
    *   ProposalID (Primary Key)
    *   PreprintID (Foreign Key)
    *   ReviewerID (Foreign Key)
    *   ProposerID (Foreign Key - UserID)
    *   Justification
    *   COIStatus
    *   COIJustification
    *   BackupReviewer (boolean)
    *   BackupJustification
    *   ProposedDate
    *   Status (Proposed, Accepted, Rejected)
*   **MiniTeamMembership:**
    *   PreprintID (Foreign Key)
    *   UserID (Foreign Key)
*   **Training:**
    *   TrainingID (Primary Key)
    *   Badge
    *   Badge Step A-Z

## 8. Technical Requirements

*   **Programming Languages:** JavaScript, Python (for backend and data processing)
*   **Frameworks:** React (for UI), Node.js/Express (for backend), any ML Framework (for the AI Suggested Reviewer algorithm).
*   **Database:** PostgreSQL or similar relational database.
*   **API:** RESTful API for communication between the frontend and backend.
*   **Authentication:** Secure user authentication and authorization.
*   **Hosting:** Cloud-based hosting (AWS, Google Cloud, Azure).
*   **Version Control:** Git with a branching strategy for development and releases.
*   **External APIs/Services:**
    *   An external API to search for reviewers and return their information (for the AI-suggested reviewer functionality, likely Profi)
    *   Potentially the Airtable API to extract data during the migration phase.

## 9. Future Considerations

*   **Improved AI-Suggested Reviewer Algorithm:**  Enhance the accuracy and relevance of the AI suggestions.
*   **Automated Reviewer Invitation:**  Automate the process of inviting reviewers based on their expertise and availability.
*   **Integration with Preprint Servers:**  Directly integrate with preprint servers to fetch metadata and monitor new preprints.
*   **Enhanced Reporting and Analytics:**  Provide more comprehensive reporting and analytics dashboards for the central team.
*   **EduTech integration:** Improve and expand the EduTech integration.
*   **Improve custom code checks:** Revamp the hacky and unreliable process of checking to see if the reviewer has already been proposed.