# Gamification & Badging System

## Overview
To motivate Student Reviewers, the system tracks key performance metrics and awards "Greenlit" status. This replaces the legacy manual tracking in Softr.

## Metrics
The following metrics are calculated from the `Student Performance` and `Selected` Airtable tables:

1.  **Total Reviews**: Count of records in `Student Reviewer Inputs` linked to the user.
2.  **Greenlit Reviews**: Count of reviews where `Status` = "Greenlit" (Approved by AE).
3.  **Greenlit Rate**: (Greenlit Reviews / Total Reviews) * 100.
4.  **Claims**: Number of active preprints claimed.

## Badges
Badges are visual indicators displayed on the Student Dashboard and Profile.

| Badge | Criteria | Description |
| :--- | :--- | :--- |
| **Novice Reviewer** | 1 Review Submitted | Completed first review. |
| **Consistent Contributor** | 5 Reviews Submitted | Active participant. |
| **Quality Star** | > 80% Greenlit Rate (min 5 reviews) | High quality submissions. |
| **Expert Reviewer** | 20+ Greenlit Reviews | Master of the domain. |

## Implementation
- **Calculation**: Calculated on-the-fly via Server Action `getStudentStats(userId)` or cached in Firestore `user_stats` collection (updated via triggers).
- **Display**: `BadgeComponent` in Shadcn/UI (Tooltip showing criteria).

