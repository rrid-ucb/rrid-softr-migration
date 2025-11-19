Okay, here's the comprehensive ISSUES AND PAIN POINTS document based on the video transcript, formatted in Markdown.

# RRID Reviewer Selection Process - Issues and Pain Points

## I. General Observations

*   **[00:19] Focus**:  The walkthrough primarily focuses on automations within the "Reviewer Selection Process" base.

![Screenshot at 00:19](../frames/frame_00002_00-19.jpg)

*   **[02:37] Goal**: The aim is to document the behind-the-scenes workings of this base and the required components.

![Screenshot at 02:37](../frames/frame_00018_02-37.jpg)

*   **[15:08, 30:25] Overall System Complexity**:  The presenter explicitly states that the overall system is "messy," needs adjustment and is needs to be rethought, suggesting significant architectural and design challenges.

## II. Problems Identified

### A. Data Inconsistencies / Integration Failures

*   **[03:11] Selected Table Sync**: An automation creates records in "Preprint Info Only" based on records in the "Selected" table. However, there's a safeguard to duplicate title and DOI information because of potential failures or changes in the "Selected" table.

![Screenshot at 03:11](../frames/frame_00023_03-11.jpg)

    *   **Impact**:  Addresses potential data loss or inconsistency between the two tables.
    *   **Workaround**:  Creating title and DOI backups.
    *   **Type:** Data Consistency, Integration.
    *   **System/Component:** Selected Table, Preprint Info Only Table.

*   **[35:35] Preprint Editorial Rejection**:

![Screenshot at 35:35](../frames/frame_00276_35-35.jpg)

    *   **Description:** When a preprint is editorially rejected, it's removed from the "Selected" base, causing linked fields in the "Preprint Info Only" base to disappear, potentially leading to loss of information about student proposals.
    *   **Impact:** Loss of data on proposed reviewers if the preprint is removed from the "Selected" base.
    *   **Workaround:** If proposals exist, the status is set to "discarded" instead of deleting the record.
    *   **Type:** Data consistency, Integration
    *   **System/Component:** Selected Table, Preprint Info Only Table.

### B. Automation Problems & Bugs

*   **[16:07] Rank Readjustment Automation**:

![Screenshot at 16:07](../frames/frame_00113_16-07.jpg)

    *   **Description**: There's an identified issue and failure with the "Rank Readjustment" automation script. The description suggests it's supposed to promote mini-team dormant preprints to active status when the invite count reaches 20, and to readjust the ranks. The speaker admits there's a failure in execution, complex logic, and need a rework to function correctly.
    *   **Impact**: Automation script that is failing to function correctly.
    *   **Type:** Bug, Automation.
    *   **System/Component:** Rank Automation Script, Preprint Info Only.
*   **[24:06] Verified first 20 Automation Delay**:

![Screenshot at 24:06](../frames/frame_00174_24-06.jpg)

    *   **Description**: Automation had to be split into 2 to function.
    *   **Type:** Bug, Automation.
    *   **System/Component:** Preprint Info Only.

## III. Pain Points

### A. Workflow Inefficiencies & Complexity

*   **[06:52] Linking Domains to Preprints**: Linking preprints to domain performance tracking is hard to do with scripts.

![Screenshot at 06:52](../frames/frame_00051_06-52.jpg)

    *   **Impact**: Requires manual effort or potentially less efficient solutions.
    *   **Type:** Workflow Inefficiency, Technical Debt.
    *   **System/Component:** Domain Performance Tracking, Preprint Info Only.
*   **[14:58] Preprint Workflow Messiness**:  The entire workflow around preprint ranking, activation, holds, and invites is described as "pretty messy," and needing adjustment.

![Screenshot at 14:58](../frames/frame_00104_14-58.jpg)

    *   **Impact**: Potential confusion, errors, and wasted time.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).
*   **[22:15] Bringing Preprint Back Alive Messiness**: Automation that brings preprints back to live needs improvement.

![Screenshot at 22:15](../frames/frame_00159_22-15.jpg)

    *   **Impact**: Redundant coding and workflow.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).
*   **[24:53] On-hold invites for reviewers and CSV issue**: The on-hold status for reviewers after the first 20 CSV emails are sent could be improved and needs follow up on if it should be active.

![Screenshot at 24:53](../frames/frame_00183_24-53.jpg)

    *   **Impact**: Redundant workflow and confusing.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).
*   **[30:00] CSV List for Reviewers**: Workflow that updates the CSV files needs to be better and that the "invited field" need to be better coded.

![Screenshot at 30:00](../frames/frame_00227_29-59.jpg)

    *   **Impact**: Redundant coding and workflow.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).
*   **[32:24] Batching Reviewers**: Automation that sends invitations to the reviewers needs to be batched.

![Screenshot at 32:24](../frames/frame_00251_32-24.jpg)

    *   **Impact**: Redundant coding and workflow.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).

### B. User Experience

*   **[10:11] Justification for Invite Formula**: A formula is used to generate the justification for invite emails because students struggled to write them correctly.

![Screenshot at 10:11](../frames/frame_00076_10-11.jpg)

    *   **Impact**: Indicates a UX issue in the reviewer proposal process, where guidance or better tools are needed for students.
    *   **Type:** UX, Training
    *   **System/Component:** Student Reviewer Input form/process.

### C. Manual Workarounds

*   **[26:40] Editorial team manually send CSVs**: Manual intervention needed and a manual process is checked to send CSVs due to inefficiencies in the original process.

![Screenshot at 26:40](../frames/frame_00196_26-40.jpg)

    *   **Impact**: Creates additional manual intervention and workload to the process.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).

### D. Confusing and unclear processes

*   **[27:59] Flag those as invited for the CSVs process**: CSV email process could be clarified.

![Screenshot at 27:59](../frames/frame_00211_27-59.jpg)

    *   **Impact**: Confusing due to unclear label.
    *   **Type:** Workflow Inefficiency, UX, Architecture.
    *   **System/Component:** Preprint Info Only (various automations related to status).

## IV. Architecture Concerns

### A. System Limitations / Technical Debt

*   **[07:06] Script Limitations**: Scripting limitations in creating linking for certain data.

![Screenshot at 07:06](../frames/frame_00053_07-06.jpg)

    *   **Impact**: Requires additional work to improve automation.
    *   **Type:** Technical Limitations.
    *   **System/Component:** Scripting Logic, Data Linking.

### B. Maintenance Challenges

*   **[21:14] Recommend looking at code to improve the workflow**: High likelihood of improvement.

![Screenshot at 21:14](../frames/frame_00152_21-14.jpg)

    *   **Impact**: Requires time and effort to improve.
    *   **Type:** Maintenance Challenges.
    *   **System/Component:** Scripting Logic, Data Linking.

## V. Additional Notes

* **Focus on Code**:  The presenter suggests referring to the code itself as the ultimate source of truth. This implies that the documentation or the conceptual understanding of the automations might be lacking.  (Multiple Timestamps)
* **Incomplete Knowledge**:  The presenter admits a lack of understanding for a weekly script. (39:18)  This raises concerns about knowledge silos and the ability to maintain the system long-term.

This document provides a solid foundation for prioritizing improvements and addressing the most critical pain points within the RRID Reviewer Selection Process.