# User Stories & Personas

## 1. Personas

### 🕵️‍♀️ Sarah - The Student Reviewer
- **Background**: PhD candidate or Postdoc looking to gain peer review experience.
- **Motivations**: Wants to complete her assigned reviews quickly to earn "Greenlit" status.
- **Frustrations**: Confusing interfaces, unclear requirements for "Justification" fields, losing work if the form doesn't save.
- **Tech Savviness**: Medium. Comfortable with web apps but expects modern UX.

### 👩‍💼 Angel - The Assistant Editor (AE)
- **Background**: Staff member managing the review pipeline.
- **Motivations**: Ensuring preprints get quality reviewers on time.
- **Frustrations**: Duplicate reviewers, incomplete data from students, difficulty finding specific preprints in a large list.
- **Tech Savviness**: Medium-High. Power user of the system.

### 👨‍💻 Reily - The Administrator
- **Background**: System owner/developer.
- **Motivations**: System stability, data integrity, accurate reporting.
- **Frustrations**: Managing user permissions manually, debugging Airtable automation failures.

## 2. User Stories

### Epic: Onboarding & Access
- **US-1**: As a **User**, I want to log in with my email and password so that I can access my personalized dashboard.
- **US-2**: As a **Student**, I want to see my "Greenlit" status on the homepage so I know if I'm meeting performance goals.

### Epic: Finding Preprints
- **US-3**: As a **Student**, I want to filter preprints by "Domain" (e.g., MedSci) so I can find articles relevant to my expertise.
- **US-4**: As a **Student**, I want to search for a preprint by title or author so I can quickly find a specific assignment.
- **US-5**: As a **Student**, I want to "Claim" a preprint from the list so that other students know I am working on it. (Constraint: Max 2 claims).

### Epic: Proposing Reviewers
- **US-6**: As a **Reviewer**, I want to propose a new reviewer by filling out a form with their details (Name, Email, Affiliation).
- **US-7**: As a **Reviewer**, I want the form to validate that I've provided a justification if the reviewer uses a generic email (Gmail/Yahoo) so that we ensure credibility.
- **US-8**: As a **Reviewer**, I want to verify if a reviewer already exists in the system before proposing them to avoid duplicates.

### Epic: Evaluating AI Suggestions
- **US-9**: As a **Reviewer**, I want to see a list of AI-suggested reviewers for a preprint so I don't have to search from scratch.
- **US-10**: As a **Reviewer**, I want to see detailed metrics (H-Index, Publication count) for an AI suggestion so I can evaluate their fit.
- **US-11**: As a **Reviewer**, I want to "Reject" an AI suggestion with a reason code so the system learns/records the decision.

### Epic: Quality Control (AE)
- **US-12**: As an **AE**, I want to view a list of all pending reviewer proposals so I can quality check them.
- **US-13**: As an **AE**, I want to "Approve" or "Reject" a student's proposal and have that status update immediately in the system.

### Epic: Dashboards
- **US-14**: As an **Admin**, I want to see a chart of "Preprints Reviewed per Week" to track overall team velocity.

