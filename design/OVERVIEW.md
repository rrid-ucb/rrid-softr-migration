# Project Overview: RRID Reviewer Selection System Migration

## 1. Purpose and Objective

The goal of this project is to migrate the existing **RRID Reviewer Selection System** from a **Softr**-based frontend to a custom **Next.js 16** application, while maintaining the robust **Airtable** backend that powers the current business logic.

This migration is driven by the need for:
- **Enhanced Customization**: Breaking free from Softr's layout constraints to build a tailored, high-performance UX for students and editors.
- **AI Integration**: Leveraging the new stack to integrate advanced AI agents ("Deep Research" capabilities) directly into the reviewer selection workflow.
- **Scalability**: Moving to a modern React framework to support future growth and complex interactive features.
- **Modern Tech Stack**: Adopting a state-of-the-art stack (Next.js App Router, React 19, Tailwind 4, Firebase) as detailed in the [Technology Stack](../rrid-app-frontend/design/TECHSTACK.md).

## 2. Stakeholders and Users

### Primary Stakeholders
- **RRID Core Team**: Responsible for the overall integrity of the peer review process.
- **Development Team**: Responsible for executing the migration and ensuring feature parity + enhancements.

### User Groups

#### 1. Administrator (e.g., Reily Fairchild)
- **Role**: Super-user managing the platform, configurations, and user permissions.
- **Goals**: Optimize workflows, monitor system health, manage user access, and ensure data integrity.
- **Key Features**: Admin dashboards, user management, system configuration.

#### 2. Assistant Editor (AE) Assignee (e.g., Editorial Staff)
- **Role**: Staff members responsible for matching preprints with qualified reviewers.
- **Goals**: Efficiently identify experts, manage conflict of interest (COI), and assign reviewers to preprints.
- **Key Features**: Advanced search/filtering of reviewers, "Propose Reviewer" workflow, AI-suggested reviewer evaluation.

#### 3. Student Reviewer (e.g., Sarah)
- **Role**: Students or early-career researchers who review preprints.
- **Goals**: Gain experience, provide high-quality feedback, and track their "Greenlit" status/productivity.
- **Key Features**: "My Quality Checks" portal, claiming preprints, submitting reviews, tracking progress.

#### 4. Central Team Member (e.g., Angel)
- **Role**: Oversees the operational aspects, ensuring preprints are moving through the pipeline.
- **Goals**: Track bottlenecks, ensure quality control, and manage the overall queue.

## 3. High-Level Scope

The migration encompasses the complete replication of the existing Softr functionality into the new Next.js application:

1.  **Landing Page**: A dashboard-style entry point navigating to key workflows (Find Preprint, Input Reviewers, Quality Checks, Progress).
2.  **Preprint Management**:
    -   Detailed lists with filtering (Domain, Status, etc.).
    -   Detailed views of individual preprints.
3.  **Reviewer Operations**:
    -   **Propose Reviewer**: Complex forms for inputting new reviewer data.
    -   **AI Suggestions**: Interface to evaluate and claim AI-suggested reviewers.
    -   **Reviewer Lists**: Searchable tables of existing reviewers.
4.  **Quality Control**: Portals for checking assigned reviews and managing status.
5.  **Dashboards**: Productivity and performance tracking for students and teams.
6.  **Auth & Security**: Replacing Softr's auth with Firebase Authentication, integrated with Airtable roles.

## 4. Success Criteria

- **Feature Parity**: All critical workflows from Softr are functioning in the new app.
- **Data Integrity**: Seamless read/write operations to the existing Airtable bases.
- **Improved UX**: Faster load times, more intuitive navigation, and better mobile responsiveness.
- **AI Readiness**: Architecture supports the immediate or future addition of "Deep Research" agents.

