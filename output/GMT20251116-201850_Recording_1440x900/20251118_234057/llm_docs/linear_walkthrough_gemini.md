Okay, here's the requested documentation of the video walkthrough, formatted in Markdown.

## Introduction to Automations in Reviewer Selection Base

*   **Key Takeaways:**
    *   The video explains the automations within the reviewer selection process base.
    *   Important tables in the base include Preprint Info Only, Student Reviewer Inputs, Referees, Recent Reviewers, and All Users.
    *   The base is used to manage preprints, reviewers, team performance, and domain performance.

*   **Description:**
    *   The speaker starts by explaining the purpose of the video: to explain the automations within the reviewer selection process base [00:15].

![Screenshot at 00:15](../frames/frame_00001_00-15.jpg)

    *   They mention that this will involve some exploration.
    *   They remind viewers of the relevant tables within the base: Preprint Info Only, Student Reviewer Inputs, Referees (AI-suggested reviewers), Recent Reviewers, All Users, Team Performance, Domain Performance, and Selected [00:26-01:34].
    *   The "All Users" table is linked to the RID app user base.
    *   The "Selected" table pulls preprints from the Rapid Reviews Infectious Disease base, specifically those that are "selected" or "to pitch editorial." [02:10-02:17]

## Walking Through Automations: From Selected to Preprint Info

*   **Key Takeaways:**
    *   The first automation creates a record in "Preprint Info Only" when a record is created in "Selected."
    *   It also updates the title and DOI, creating backup information.
    *   A script pulls ranking and team assignment data, updating the rank accordingly.

*   **Description:**
    *   The speaker begins walking through each automation, explaining its purpose and how it achieves it [02:37].

![Screenshot at 02:37](../frames/frame_00018_02-37.jpg)

    *   The first automation triggers "when a record is created in Selected." This means a preprint has been flagged as selected by the editorial team [02:57].

![Screenshot at 02:57](../frames/frame_00021_02-57.jpg)

    *   The automation creates a corresponding record within the "Preprint Info Only" table.  It links to the "Selected" table and updates the title and DOI [03:11].

![Screenshot at 03:11](../frames/frame_00023_03-11.jpg)

    *   A script is run to get important information like ranking and assigned team from the selected record [03:50-04:05].
    *   The script then determines whether the rank needs to be updated. If the editorial team hasn't assigned a rank, it's set to "NA" [04:20].

![Screenshot at 04:20](../frames/frame_00032_04-20.jpg)

    *   If the assigned team is updated, that information is also updated [05:06].

![Screenshot at 05:06](../frames/frame_00037_05-06.jpg)


*   **UI Elements/Interactions:**
    *   Airtable UI is shown, displaying automation triggers, actions, and configuration options.
    *   The UI shows linked fields and single select fields being configured.

## Tracking Team Performance and Domain Performance

*   **Key Takeaways:**
    *   An automation creates a record in the "Referees" table when someone pitches a preprint and suggests a reviewer.
    *   Another automation tracks team performance by linking proposed reviewers to the team they are associated with, considering domain for Berkeley teams.
    *   Domain performance is tracked by linking preprints to the domain performance table.

*   **Description:**
    *   A record is created within the "Referees" table when someone pitches a preprint and suggests an ideal reviewer.  This information is pushed into the suggested reviewer table [05:17].

![Screenshot at 05:17](../frames/frame_00039_05-17.jpg)

    *   The "Track Team Performance" automation links proposed reviewers to the team they're associated with.  For Berkeley, it considers both the country and the domain [05:50-06:05].
    *   If it's not Berkeley, the proposed reviewer is simply linked to the team the student is associated with [06:24].

![Screenshot at 06:24](../frames/frame_00046_06-24.jpg)

    *   When a record is created within "Preprint Info Only," the automation finds the record in "Domain Performance" with the same domain and links it [06:45-06:59].
    *   Team performance is updated with the preprint info. This tracks students' contributions to their team and the preprints that teams are pitching [07:13].

![Screenshot at 07:13](../frames/frame_00055_07-13.jpg)


## Automations Related to Student Reviewer Inputs (SRI)

*   **Key Takeaways:**
    *   When a record is created in Student Reviewer Inputs, the automation finds the associated preprint ID and links the student to the All Users base.
    *   The automation updates the link to publications using a formula field.

*   **Description:**
    *   The speaker transitions to automations triggered by records created in "Student Reviewer Inputs" (SRI), where reviewers are proposed [08:04].

![Screenshot at 08:04](../frames/frame_00061_08-04.jpg)

    *   The automation finds the associated preprint ID in the "Preprint Info Only" table [08:19].

![Screenshot at 08:19](../frames/frame_00064_08-19.jpg)

    *   It links the student who proposed the reviewer to the "All Users" base to track productivity [08:23].

![Screenshot at 08:23](../frames/frame_00065_08-23.jpg)

    *   It uses an auto-update for the link to the publication, utilizing a formula field with the reviewer's name to create a link to publications on PubMed [08:39-08:53].
    *   The speaker notes that there was a misplaced automation [09:18-09:26].
    *   The automation also attaches the associated record to "Preprint Info Only," linking the preprint to the proposed reviewer [09:39].

![Screenshot at 09:39](../frames/frame_00073_09-39.jpg)


## Automations for Quality Checking and COI (Conflict of Interest)

*   **Key Takeaways:**
    *   When proposed reviewers are updated, the automation tracks key fields like "justification for invite," quality checker emails, and updates relevant links.
    *   An immediate COI checker verifies that the reviewer isn't the author, already proposed, or a recent reviewer, and flags duplicate domains.
    *   The COI checker also removes AI-suggested reviewers with the same domain.

*   **Description:**
    *   The speaker discusses automations triggered when proposed reviewers' fields are updated, focusing on "justification for invite," the email of the quality checker, and the email of the quality checker in training [09:52-10:26].
    *   The "Immediate Reviewer COI Checker" makes sure the reviewer isn't the author, hasn't already been proposed, and isn't a recent reviewer [10:53].

![Screenshot at 10:53](../frames/frame_00081_10-53.jpg)

    *   It checks for duplicate domains and flags them [11:11].

![Screenshot at 11:11](../frames/frame_00083_11-11.jpg)

    *   It also removes AI-suggested reviewers with the same domain [11:26].

![Screenshot at 11:26](../frames/frame_00085_11-26.jpg)


## Managing Preprint Ranking and Status

*   **Key Takeaways:**
    *   The "Stef Ranking" automation updates the rank inputted by Stef, taking into account other preprints on hold with higher rankings.
    *   The automation to populate AI-suggested reviewers parses through the referee info, extracts details, and builds a record for each AI-suggested reviewer.

*   **Description:**
    *   The speaker describes automations related to preprint ranking, making a preprint active or on hold, and sending out invites, admitting it's messy [11:36-11:57].
     *   The "Stef Ranking" automation adjusts the rank inputted by Stef based on whether other preprints are on hold and have higher rankings [11:57].

![Screenshot at 11:57](../frames/frame_00089_11-57.jpg)

    *   The automation to populate AI-suggested reviewers (referees) parses through the referee info when it's not empty. It extracts their name, H-index, affiliations, ORCID ID, author URL, and emails using regex [12:26-13:03].
    *   It checks if the referee shouldn't be an option based on whether they're in recent reviewers or have a common domain [13:03].

![Screenshot at 13:03](../frames/frame_00098_13-03.jpg)

    *   A record is added for each reviewer in the referees table [13:21].

![Screenshot at 13:21](../frames/frame_00099_13-21.jpg)


## Complex Logic for Preprint Status and Invites

*   **Key Takeaways:**
    *   When a rank is zero and the preprint status is active, the automation sets both to true.
    *   When the invite count hits 20 for a dormant preprint, the automation makes it active.
    *   Automations manage preprint status (on hold, out of circulation) based on invite counts and quality checks.

*   **Description:**
    *   The speaker moves into automations related to preprint ranking and the flow of making a preprint active, on hold, sending out invites [14:43].

![Screenshot at 14:43](../frames/frame_00103_14-43.jpg)

    *   If a rank is zero and the preprint status is active, it sets both to true.  If it's the first time being active, it sets the status to "in process" and updates the date [15:15-15:50].
    *   When the invite count is greater than or equal to 20 and the preprint status is dormant, it's supposed to make the preprint active immediately [16:15-16:56].
    *   The speaker mentions a complex logic behind adjusting the ranks [17:20].

![Screenshot at 17:20](../frames/frame_00123_17-20.jpg)

    *   Setting the preprint status to "on hold" is based on a formula called "more invites needed," which considers the invite round, total invite count, and unchecked count [17:34-18:52].
    *   If no additional invites are needed, the preprint is set to "on hold" and "out of circulation" [19:10].

![Screenshot at 19:10](../frames/frame_00136_19-10.jpg)

    *   Once a preprint is on hold, the automation finds other preprints in that domain and makes sure at least one is active [19:34]. The automation considers ranking, status (dormant vs. on hold), invite count, date in process, and Stef's ranking [19:47-21:07].

![Screenshot at 19:34](../frames/frame_00140_19-34.jpg)

    *   If a preprint is on hold, but quality checking indicates it doesn't need more invites, the rank is set to "out of circulation" [21:40-21:59].
    *   If a preprint is in circulation but all unchecked reviewers are rejected, and more invites are needed, the preprint is immediately made active [22:15-22:40].

## Managing Invite Processes and COI Checks

*   **Key Takeaways:**
    *   If a preprint is dormant, active, or on hold, and unsent invites are above 20, the automation checks for COI and verifies the first 20 invites.
    *   Multiple automations handle sending invites and ensuring COI checks are performed at different stages of the invite process.
    *   A manual send invite option allows editorial staff to force send invites, also with COI checks.

*   **Description:**
    *   The speaker continues discussing the flow when a preprint receives invites [23:06].

![Screenshot at 23:06](../frames/frame_00165_23-06.jpg)

    *   If a preprint is dormant, active, or on hold, unsent invites is >= 20, it's selected, and it's the first invite round, the automation checks that none of the proposed reviewers are authors or recent reviewers [23:14-23:31].
    *   It verifies the first 20, then the preprint is put on hold and re-ranked [23:58-24:31].
    *   If invite count > 30 and total unsent > 10 and unchecked = 0, another COI check is run [25:36]. The invite round is updated, determined by the invite count.

![Screenshot at 25:36](../frames/frame_00188_25-36.jpg)

    *   A "Manual Send Invites" option allows someone on the editorial team to force send the CSVs [26:40-26:57].
    *   For manually sent invites, if there's a non-zero amount of unsent invites, a COI check is performed. The automated checks are verified, and then the Google Cloud function is triggered to send the invites [27:02].

![Screenshot at 27:02](../frames/frame_00200_27-02.jpg)

    *   The automation finds records that have not been checked as invited and flags them as invited [27:47].

![Screenshot at 27:47](../frames/frame_00208_27-47.jpg)


## Finalizing Invites and Limiting Claims

*   **Key Takeaways:**
    *   When the invite count is above 30 and there are no unchecked reviewers, the preprint is considered complete, updating its status.
    *   To prevent students from claiming too many AI-suggested reviewers, the automation limits them to 3 claims.

*   **Description:**
    *   If the invite count is > 30 and unchecked is 0, a COI is run again [28:12].

![Screenshot at 28:12](../frames/frame_00214_28-12.jpg)

    *   The preprint is updated to complete and out of circulation. This will push all reviewers to a CSV, but their invited field needs to be unchecked to get the full list [29:35].

![Screenshot at 29:35](../frames/frame_00224_29-35.jpg)

    *   For AI-suggested reviewers, students can claim reviewers, but are limited to 3 claims [30:27].

![Screenshot at 30:27](../frames/frame_00233_30-27.jpg)

    *   If a student claims more than 2, the automation removes the oldest claimed reviewer, making it unable to evaluate [30:49].

![Screenshot at 30:49](../frames/frame_00236_30-49.jpg)


## Post-Invite Actions and Clean-Up

*   **Key Takeaways:**
    *   When a preprint is complete, assistant editor columns are cleared for cleaner tracking.
    *   Automations track and delete recent reviewers, invite AI reviewers, and prevent inviting reviewers proposed in other preprints within a short timeframe.

*   **Description:**
    *   When a preprint is complete (invite count is 40, is marked as invited), the automation clears assistant editor columns. This makes tracking cleaner [31:10-31:47].
    *   When a preprint is invited or complete and is invited to track reviewers [32:06], the automation creates a record.

![Screenshot at 32:06](../frames/frame_00248_32-06.jpg)

    *   It tracks recent reviewers to prevent inviting them again until 3 months after [32:47]. Those that requested not to be are deleted [32:56].

![Screenshot at 32:47](../frames/frame_00255_32-47.jpg)

    *   If an assistant editor proposes a reviewer and doesn't mark it as incomplete, the reviewer is immediately set to invite, assuming the assistant editor has verified suitability [33:15].

![Screenshot at 33:15](../frames/frame_00259_33-15.jpg)

    *   If a reviewer is flagged as invite, the automation makes sure they haven't been proposed in other preprints [33:58].

![Screenshot at 33:58](../frames/frame_00264_33-58.jpg)

    *   If an invited reviewer is from berkeley.edu, the automation removes others from the same domain in the AI-suggested reviewers [34:33].

![Screenshot at 34:33](../frames/frame_00268_34-33.jpg)


## Tracking and Managing Reviewers and Preprints

*   **Key Takeaways:**
    *   The automation tracks student reviewer productivity, updating user productivity when AI referees are rejected or proposed.
    *   When a preprint is editorially rejected, its status is updated to discarded, or the record is deleted.
    *   Daily summary emails are sent with information on rejects, unchecked counts, and AI reviewer status.

*   **Description:**
    *   The automation tracks student reviewer productivity, inputting the student email and associating it with their user productivity when the status in the AI referee table is "reject" or "proposed" [34:59].

![Screenshot at 34:59](../frames/frame_00271_34-59.jpg)

    *   If a preprint is editorially rejected, it is no longer in the selected base [35:31]. If no one has proposed reviewers for it, the record is deleted. If people have proposed reviewers, the preprint status is set to discarded [35:54].

![Screenshot at 35:31](../frames/frame_00275_35-31.jpg)

    *   Daily reject summaries are sent via Google Cloud function, including quality check comments and whether a reviewer is fixable. The goal is to provide summaries rather than individual emails [36:27].

![Screenshot at 36:27](../frames/frame_00283_36-27.jpg)

    *   If any preprints have an unchecked count greater than 10, an email summary is sent daily at 8 AM to assistant editors associated with that domain [37:41].

![Screenshot at 37:41](../frames/frame_00292_37-41.jpg)

    *   If the unchecked count is greater than 30, Stef is also flagged [38:13].

![Screenshot at 38:13](../frames/frame_00297_38-13.jpg)

    *   The automation checks to see if AI reviewers high reject counts or low numbers of remaining AI reviewers and sends help emails to those responsible for that task [38:25].

![Screenshot at 38:25](../frames/frame_00300_38-25.jpg)

    *   If unclaimed AI reviewers are less than 15, a "go help out" email is sent [39:05].

![Screenshot at 39:05](../frames/frame_00306_39-05.jpg)

    *   The speaker notes the presence of an automation they did not create related to weekly reports, showing how it finds email lists for the recipients. [39:18-40:38].

This should provide a very detailed, well-structured breakdown of the video walkthrough! Let me know if you need any adjustments.