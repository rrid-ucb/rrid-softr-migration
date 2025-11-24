# AI & Agentic Architecture

## Overview
The system leverages Google's Gemini models (via Firebase Genkit or Vercel AI SDK) to enhance the reviewer selection process. This document outlines the "Deep Research" agent capabilities and the development environment.

## 1. Development Environment: Google Antigravity
We are building this application using **Google Antigravity**, an AI-first IDE.
- **Role**: The IDE acts as a pair programmer, generating boilerplate, refactoring code, and enforcing the specs defined in `design/`.
- **Agents**: We will define custom agents within Antigravity to handle:
    - **Schema Sync**: Agent to watch `airtable_schema_report.md` and update Zod schemas.
    - **Test Gen**: Agent to generate unit tests for new components.

## 2. Feature: "Deep Research" Agent
**Goal**: Automate the validation of potential reviewers.

### Workflow
1.  **Trigger**: User clicks "Analyze Reviewer" on a proposal or AI suggestion.
2.  **Agent Action**:
    -   **Search**: Queries PubMed/Google Scholar for recent publications.
    -   **COI Check**: Checks for co-authorship with Preprint authors in the last 3 years.
    -   **Expertise Match**: Compares Preprint Abstract embedding with Reviewer's publication abstract embeddings.
3.  **Output**: Returns a "Confidence Score" and a summary of potential conflicts.

### Implementation
-   **Framework**: Firebase Genkit (Node.js).
-   **Model**: `gemini-3-pro-preview`.
-   **Tools**:
    -   `pubmed_search`: Tool to query PubMed API.
    -   `vector_search`: Tool to query Firestore Vector Store.

## 3. AI Suggested Reviewers
**Current State**: "Parsing algorithm" (custom script).
**Future State**:
-   Replace brittle scripts with a structured LLM extraction pipeline.
-   Input: PDF/Text of Preprint.
-   Output: JSON list of candidate reviewers (extracted from References + External Search).

