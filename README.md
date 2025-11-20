# RRID Softr Migration - Video Annotation System

Transform video walkthroughs into comprehensive product documentation using AI-powered analysis.

## Table of Contents

- [Generated Documentation](#generated-documentation)
  - [Softr Application Walkthrough](#softr-application-walkthrough)
    - [Softr Linear Walkthrough](#-softr-linear-walkthrough)
    - [Softr Personas, User Stories, and User Journeys](#-softr-personas-user-stories-and-user-journeys)
    - [Softr Product Requirements Document (PRD)](#-softr-product-requirements-document-prd)
    - [Softr Issues & Pain Points](#-softr-issues--pain-points)
  - [Airtable Backend Walkthrough](#airtable-backend-walkthrough)
    - [Airtable Linear Walkthrough](#-airtable-linear-walkthrough)
    - [Airtable Personas, User Stories, and User Journeys](#-airtable-personas-user-stories-and-user-journeys)
    - [Airtable Product Requirements Document (PRD)](#-airtable-product-requirements-document-prd)
    - [Airtable Issues & Pain Points](#-airtable-issues--pain-points)
- [What This Does](#what-this-does)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Example Use Case](#example-use-case-softr-migration)
- [What You Need](#what-you-need)
- [File Structure](#file-structure)
- [Usage Examples](#usage-examples)
- [Output Documents Explained](#output-documents-explained)
- [Cost](#cost)
- [Tips for Best Results](#tips-for-best-results)
- [Troubleshooting](#troubleshooting)
- [Project Status](#project-status)

## Generated Documentation

This project has generated comprehensive documentation from two video walkthroughs:

1. **Softr Application Walkthrough** - Frontend user interface and workflows
2. **Airtable Backend Walkthrough** - Backend architecture, automations, and integrations

### Softr Application Walkthrough

Documentation from the Softr application walkthrough providing detailed analysis of the RRID Reviewer Selection system frontend.

> **Note:** These documents represent the best available versions based on comprehensive comparison. The Linear Walkthrough uses the enriched version for superior technical detail, while PRD, Personas, and Issues use the latest Gemini-generated versions for maximum comprehensiveness. See [COMPARISON_ANALYSIS.md](COMPARISON_ANALYSIS.md) for detailed comparison of all document versions.

#### 📖 [Softr Linear Walkthrough](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md)

A comprehensive, chapter-by-chapter walkthrough of the Softr application that goes beyond the speaker's narration to identify interface components, Airtable integrations, and UI details. Perfect for understanding the complete application flow and training new team members.

**Table of Contents:**
- [Chapter 1: Overview of the RID Reviewer Selection Softr Application Structure and Landing Page](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-1-overview-of-the-rid-reviewer-selection-softr-application-structure-and-landing-page) - Application structure, landing page, and role-based views
- [Chapter 2: Exploring Preprint Lists and Role-Based Visibility](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-2-exploring-preprint-lists-and-role-based-visibility) - Preprint management with conditional filters and role-based access
- [Chapter 3: Examining Preprint Details and Reviewer Proposal Workflow](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-3-examining-preprint-details-and-reviewer-proposal-workflow) - Detailed preprint views, AI-suggested reviewers, and COI checks
- [Chapter 4: Dynamic Form Validation and Reviewer Matching using Custom Code](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-4-dynamic-form-validation-and-reviewer-matching-using-custom-code) - Custom JavaScript validation and reviewer matching logic
- [Chapter 5: Evaluating and Managing AI-Suggested Reviewers](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-5-evaluating-and-managing-ai-suggested-reviewers) - AI reviewer evaluation workflow and status management
- [Chapter 6: Reviewer Proposal and Quality Check Workflow](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-6-reviewer-proposal-and-quality-check-workflow) - Quality check portals and reviewer proposal management
- [Chapter 7: Central Team Management and Data Control](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-7-central-team-management-and-data-control) - Administrative dashboards and data management interfaces
- [Chapter 8: Central Team Dashboards: Productivity and Training](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-8-central-team-dashboards-productivity-and-training) - Productivity tracking and achievement/training dashboards
- [Chapter 9: Tracking Progress and Configuring Header Navigation](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md#chapter-9-tracking-progress-and-configuring-header-navigation) - Student progress tracking and navigation configuration

#### 👥 [Softr Personas, User Stories, and User Journeys](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md)

Comprehensive user-centric documentation identifying three distinct personas (Sarah - Student Reviewer, David - Assistant Editor, Angel - Central Team Member) with detailed backgrounds, goals, pain points, and how they interact with the system. Includes extensive user stories with acceptance criteria, feature mapping, and complete user journeys.

**Table of Contents:**
- [User Personas](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md#1-user-personas) - Three detailed personas: Sarah (Student Reviewer), David (Assistant Editor), and Angel (Central Team Member) with comprehensive backgrounds, goals, motivations, and technical skill levels
- [User Stories](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md#2-user-stories) - Feature-specific user stories organized by page/feature (Landing Page, Preprints List, Article Details, Quality Check Portal, etc.) with acceptance criteria and priority levels
- [Feature Mapping](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md#3-feature-mapping) - Mapping of features to personas and their access levels
- [User Journeys](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md#4-user-journeys) - Complete workflows: Sarah proposing a reviewer, David quality checking a proposed reviewer, and Angel updating preprint status
- [Screenshots and Context](output/softr/20251119_071215/llm_docs/personas_stories_gemini.md#5-screenshots-and-context) - Visual anchors supporting user stories and journeys

#### 📋 [Softr Product Requirements Document (PRD)](output/softr/20251119_071215/llm_docs/prd_document_gemini.md)

A comprehensive PRD with detailed page-by-page specifications covering 20+ pages, technical requirements, complete data models, and user workflows. Essential for development planning, technical specifications, and migration projects. This is the most complete PRD available, covering all pages visible in the video walkthrough.

**Table of Contents:**
- [Executive Summary](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#executive-summary) - System overview and key features
- [Introduction, Goals, Target Audience, Scope](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#1-introduction) - Project context and objectives
- [Functional Requirements](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#5-functional-requirements) - Detailed specs for 20+ pages including Landing Page, Preprints List, Article Details, Quality Check Portal (multiple variants), Training pages, Dashboards, and more
- [Non-Functional Requirements](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#6-non-functional-requirements) - Performance, scalability, and quality requirements
- [Data Model](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#7-data-model) - Complete data structures for all entities
- [Technical Requirements](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#8-technical-requirements) - Platform, database, authentication, APIs, and security requirements
- [Future Considerations](output/softr/20251119_071215/llm_docs/prd_document_gemini.md#9-future-considerations) - Potential enhancements and improvements

#### ⚠️ [Softr Issues & Pain Points](output/softr/20251119_071215/llm_docs/issues_gemini.md)

A comprehensive catalog of problems, pain points, and technical concerns identified in the Softr application. Documents bugs, workflow inefficiencies, system limitations, and suggested solutions.

**Table of Contents:**
- [Problems Identified](output/softr/20251119_071215/llm_docs/issues_gemini.md#1-problems-identified) - Data parsing failures, email mapping issues, and technical bugs
- [Pain Points](output/softr/20251119_071215/llm_docs/issues_gemini.md#2-pain-points) - Learning curve, naming standards, outdated help, race conditions, custom code rendering, and tracking gaps
- [Architecture Concerns](output/softr/20251119_071215/llm_docs/issues_gemini.md#3-architecture-concerns) - Hacky custom code, AirTable dependencies, hardcoded components, and automation gaps
- [System/Component Categorization](output/softr/20251119_071215/llm_docs/issues_gemini.md#4-systemcomponent-categorization) - Summary table of issues by system component

### Airtable Backend Walkthrough

Documentation from the Airtable backend walkthrough providing detailed analysis of automations, table structures, integrations, and system architecture.

#### 📖 [Airtable Linear Walkthrough](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md)

A comprehensive walkthrough of the Airtable backend automations and workflows that power the reviewer selection process. Documents each automation, its triggers, actions, and business logic.

**Table of Contents:**
- [Introduction to Automations in Reviewer Selection Base](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#introduction-to-automations-in-reviewer-selection-base) - Overview of tables and base structure
- [Walking Through Automations: From Selected to Preprint Info](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#walking-through-automations-from-selected-to-preprint-info) - Initial automation workflows
- [Tracking Team Performance and Domain Performance](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#tracking-team-performance-and-domain-performance) - Performance tracking automations
- [Automations Related to Student Reviewer Inputs (SRI)](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#automations-related-to-student-reviewer-inputs-sri) - Student workflow automations
- [Automations for Quality Checking and COI (Conflict of Interest)](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#automations-for-quality-checking-and-coi-conflict-of-interest) - Quality assurance workflows
- [Managing Preprint Ranking and Status](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#managing-preprint-ranking-and-status) - Status management automations
- [Complex Logic for Preprint Status and Invites](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#complex-logic-for-preprint-status-and-invites) - Advanced workflow logic
- [Managing Invite Processes and COI Checks](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#managing-invite-processes-and-coi-checks) - Reviewer invitation workflows
- [Finalizing Invites and Limiting Claims](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#finalizing-invites-and-limiting-claims) - Invitation completion processes
- [Post-Invite Actions and Clean-Up](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#post-invite-actions-and-clean-up) - Post-processing automations
- [Tracking and Managing Reviewers and Preprints](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/linear_walkthrough_gemini.md#tracking-and-managing-reviewers-and-preprints) - Ongoing management workflows

#### 👥 [Airtable Personas, User Stories, and User Journeys](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/personas_stories_gemini.md)

User-centric documentation for the Airtable backend system, identifying personas (Editorial Lead, Assistant Editor, Student Reviewer Proposer), their goals, pain points, and how they interact with automations.

**Table of Contents:**
- [User Personas](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/personas_stories_gemini.md#1-user-personas) - Editorial Lead (Stef), Assistant Editor (Angel), Student Reviewer Proposer, and AI Model personas
- [User Stories](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/personas_stories_gemini.md#2-user-stories) - 14 automation-specific user stories with acceptance criteria
- [Feature Mapping](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/personas_stories_gemini.md#3-feature-mapping) - Mapping of automations to personas and their access levels
- [User Journeys](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/personas_stories_gemini.md#4-user-journeys) - Complete workflows for preprint processing and quality checking

#### 📋 [Airtable Product Requirements Document (PRD)](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md)

A comprehensive PRD documenting all Airtable tables, automations, data models, and technical requirements. Essential for understanding the backend architecture and rebuilding the system.

**Table of Contents:**
- [Executive Summary](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md#1-executive-summary) - System overview and key features
- [Pages and Features](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md#7-pages-and-features) - Detailed specs for 37 automations and 9 data tables
- [Technical Requirements](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md#8-technical-requirements) - Platform, scripting, and integration requirements
- [Data Model](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md#10-data-model) - Complete data structures for all tables
- [User Interactions and Workflows](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/prd_document_gemini.md#9-user-interactions-and-workflows) - Step-by-step automation workflows

#### ⚠️ [Airtable Issues & Pain Points](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md)

A comprehensive catalog of problems, pain points, and technical concerns identified in the Airtable backend system. Documents bugs, workflow inefficiencies, system limitations, and suggested solutions.

**Table of Contents:**
- [General Observations](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md#i-general-observations) - Overall system complexity and concerns
- [Problems Identified](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md#ii-problems-identified) - Data inconsistencies, integration failures, and automation bugs
- [Pain Points](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md#iii-pain-points) - Workflow inefficiencies, UX issues, and manual workarounds
- [Architecture Concerns](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md#iv-architecture-concerns) - System limitations, technical debt, and maintenance challenges
- [Additional Notes](output/GMT20251116-201850_Recording_1440x900/20251118_234057/llm_docs/issues_gemini.md#v-additional-notes) - Knowledge gaps and documentation concerns

## What This Does

Takes a video walkthrough (like a product demo or UI tour) and automatically generates:

1. **Linear Walkthrough** - Organized chapters with key takeaways and timestamps
2. **PRD Document** - Page-by-page specs for rebuilding the application  
3. **Personas & User Stories** - User-centric documentation with acceptance criteria
4. **Issues & Pain Points** - For backend/architecture videos, catalogs problems, bugs, and technical debt

All with screenshots, timestamps, and detailed UI descriptions.

## Quick Start

```bash
# 1. Setup virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Set API keys
export GEMINI_API_KEY="your_key"
export OPENAI_API_KEY="your_key"

# 3. Process a video
./process_video.sh design/your-video.mp4
```

**For subsequent sessions:**
```bash
source venv/bin/activate
```

That's it! You'll get comprehensive documentation in `output/{video_name}/{run_timestamp}/docs/`.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide (start here!)
- **[COMPARISON_ANALYSIS.md](COMPARISON_ANALYSIS.md)** - Detailed comparison of all document versions (enriched vs latest Gemini vs OpenAI)
- **[docs/](docs/)** - Comprehensive documentation
  - `LLM_ANNOTATION_README.md` - Complete LLM documentation guide
  - `VIDEO_ANNOTATION_README.md` - Basic transcription workflow
  - `FRAME_EXTRACTION_README.md` - Frame extraction guide
  - `REFACTORING_GUIDE.md` - New system structure
  - And more...
- **[design/](design/)** - Design and planning documents

## Example Use Case: Softr Migration

This project was created to document an existing Softr application for migration. The workflow:

1. Record a comprehensive walkthrough of the Softr app
2. Run the annotation pipeline to generate documentation
3. Use the generated PRD for rebuilding in a new platform
4. Reference personas/user stories for product planning

### Airtable Backend Documentation

In addition to documenting the Softr frontend, this project also processes videos about the Airtable backend architecture, automations, and integrations. These videos help understand:

- **Airtable Architecture**: Table structures, relationships, and data models
- **Automations**: Workflow automation logic and triggers
- **Integration Points**: How Softr interfaces with Airtable
- **Issues & Pain Points**: Problems, workarounds, and technical debt documented in `ISSUES.md`

The pipeline automatically detects when a video includes backend/architecture content and generates an additional `issues.md` document cataloging problems, pain points, and technical concerns.

## What You Need

### System Requirements
- macOS (tested) or Linux
- Python 3.8+
- ~5GB disk space for models

### Dependencies
```bash
# System dependencies
brew install openai-whisper ffmpeg

# Python dependencies (in virtual environment)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Keys (for LLM processing)
- **Gemini**: https://aistudio.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys

```bash
export GEMINI_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

## File Structure

```
.
├── README.md                    # This file
├── QUICKSTART.md                # Quick reference
├── LLM_ANNOTATION_README.md     # Full documentation
├── VIDEO_ANNOTATION_README.md   # Basic workflow docs
├── requirements.txt             # Python dependencies
│
├── annotate_video.py            # Step 1: Basic annotation
├── llm_annotate.py              # Step 2: LLM processing
├── process_video.sh             # All-in-one pipeline
├── setup_and_test.sh            # Setup & testing
│
├── venv/                        # Virtual environment (created by setup)
├── design/                      # Input videos
│   └── softr.mp4
│
└── output/                      # Generated output (run-based structure)
    └── {video_name}/            # Per-video outputs
        └── {run_timestamp}/     # Timestamped runs
            ├── frames/          # Extracted screenshots
            ├── transcripts/     # Transcripts and annotations
            └── docs/            # AI-generated docs by model
                ├── openai/
                │   ├── linear_walkthrough.md
                │   ├── prd_document.md
                │   └── personas_stories.md
                ├── gemini_vision/
                │   ├── linear_walkthrough.md
                │   ├── prd_document.md
                │   └── personas_stories.md
                └── ...
```

## Usage Examples

**Always activate venv first:**
```bash
source venv/bin/activate
```

### Process with default settings
```bash
./process_video.sh design/video.mp4
```

### Better quality transcription
```bash
./process_video.sh design/video.mp4 medium
```

### Use only Gemini (faster/cheaper)
```bash
./process_video.sh design/video.mp4 base gemini
```

### Best quality with both LLMs
```bash
./process_video.sh design/video.mp4 large "gemini openai"
```

### Process existing transcript with LLMs
```bash
python3 llm_annotate.py out/annotated.json --models gemini openai
```

### Process videos with existing transcripts (Zoom, etc.)
The pipeline automatically detects and uses existing transcript files:
- **VTT files**: `.transcript.vtt`, `.cc.vtt`, `.vtt` (WebVTT format)
- **JSON files**: Already in Whisper format
- **Text files**: Basic support (may fall back to Whisper)

When a transcript is found in the same directory as the video, the pipeline:
1. Converts VTT to Whisper JSON format (if needed)
2. Skips Whisper transcription
3. Proceeds with frame extraction and LLM processing

Example: Zoom recordings typically include `.transcript.vtt` files that are automatically detected and used.

## Output Documents Explained

### 1. Linear Walkthrough
Follows the video chronologically with chapters, topics, and key takeaways. Great for:
- Understanding the application flow
- Training new team members  
- Creating user documentation
- Feature overviews

### 2. PRD Document
Page-by-page breakdown with UI components, features, and business logic. Use for:
- Development planning
- Technical specifications
- Migration projects
- Competitive analysis

### 3. Personas & User Stories
User-centric view with personas, stories, and acceptance criteria. Ideal for:
- Product planning
- UX design decisions
- Feature prioritization
- Stakeholder communication

### 4. Issues & Pain Points (ISSUES.md)
For backend/architecture videos, catalogs:
- Technical problems and bugs
- Workflow inefficiencies
- System limitations and technical debt
- Integration and automation issues
- User experience pain points
- Suggested solutions and workarounds

## Cost

- **Whisper** (local): Free
- **FFmpeg** (local): Free
- **Gemini API**: ~$0.50-2.00 per 30-min video
- **OpenAI API**: ~$1.00-3.00 per 30-min video

Typical 30-minute walkthrough costs $1-5 total to process with both models.

## Tips for Best Results

### Recording Your Video
1. Speak clearly and describe what you're doing
2. Go slowly and pause at important screens
3. Navigate through all pages and features
4. Explain user roles, workflows, and business logic
5. Show validation, errors, and edge cases

### Optimizing Output
1. Use `medium` or `large` Whisper model for better transcription
2. Lower scene threshold (0.20) for more screenshots
3. Record in a quiet environment
4. Compare Gemini vs OpenAI outputs
5. Edit the generated markdown for final polish

## Troubleshooting

Run the setup script to check your environment:
```bash
./setup_and_test.sh
```

Common issues:
- **"GEMINI_API_KEY not set"** → `export GEMINI_API_KEY="your_key"`
- **"No module named 'google'"** → Activate venv: `source venv/bin/activate`
- **Missing packages** → `source venv/bin/activate && pip install -r requirements.txt`
- **Poor transcription** → Use larger Whisper model or record in quieter environment
- **Frames not matching** → Try lower scene threshold or fixed interval extraction

See [LLM_ANNOTATION_README.md](LLM_ANNOTATION_README.md) for detailed troubleshooting.

## Project Status

✅ Basic transcription with Whisper  
✅ Frame extraction with ffmpeg  
✅ Timestamp annotation  
✅ LLM-powered documentation generation  
✅ Multiple LLM provider support (Gemini, OpenAI)  
✅ Three document types (walkthrough, PRD, personas)  
✅ Issues document generation for backend/architecture videos  
✅ VTT transcript support (Zoom, WebVTT)  
✅ Automatic transcript detection and conversion  
✅ Comparison mode for LLM outputs  

## Contributing

This is a migration project tool, but feel free to adapt it for your own use cases:
- Product demos
- UI/UX documentation
- Competitive analysis
- Feature documentation
- Training materials

## License

Scripts and documentation: MIT License

Dependencies have their own licenses:
- OpenAI Whisper: MIT
- FFmpeg: GPL/LGPL
- Google Generative AI SDK: Apache 2.0
- OpenAI Python SDK: MIT
