# RRID Softr Migration - Video Annotation System

Transform video walkthroughs into comprehensive product documentation using AI-powered analysis.

## Generated Documentation

This project has generated comprehensive documentation from a Softr application walkthrough. The following enriched documents provide detailed analysis of the RRID Reviewer Selection system:

### 📖 [Linear Walkthrough](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/linear_walkthrough_enriched.md)

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

### 👥 [Personas, User Stories, and User Journeys](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/personas_stories_enriched.md)

User-centric documentation identifying three distinct personas (Administrator, AE Assignee, Reviewer), their goals, pain points, and how they interact with the system. Includes detailed user stories with acceptance criteria and complete user journeys.

**Table of Contents:**
- [User Personas](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/personas_stories_enriched.md#1-user-personas) - Three personas: Administrator, AE Assignee, and Reviewer with detailed backgrounds, goals, and technical skill levels
- [User Stories](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/personas_stories_enriched.md#2-user-stories) - Feature-specific user stories with acceptance criteria and priority levels
- [Feature Mapping](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/personas_stories_enriched.md#3-feature-mapping) - Mapping of features to personas and their access levels
- [User Journeys](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/personas_stories_enriched.md#4-user-journeys) - Complete workflows for Administrator customization, AE reviewer assignment, and Reviewer preprint claiming

### 📋 [Product Requirements Document (PRD)](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md)

A comprehensive PRD with page-by-page specifications, technical requirements, data models, and user workflows. Essential for development planning, technical specifications, and migration projects.

**Table of Contents:**
- [Executive Summary](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md#1-executive-summary) - System overview and key features
- [Page-by-Page Specifications](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md#2-page-by-page-specifications) - Detailed specs for Landing Page, Preprints List, Reviewer Proposal, AI Suggestions, Quality Checks, and more
- [Technical Requirements](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md#3-technical-requirements) - Platform, database, authentication, APIs, and security requirements
- [Data Models](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md#4-data-models-inferred) - Inferred data structures for Preprints, Reviewers, Users, and Review Assignments
- [User Workflows](https://github.com/rrid-ucb/rrid-softr-migration/blob/main/out/llm_docs_enriched/prd_document_enriched.md#5-user-workflows) - Step-by-step workflows for adding reviewers, evaluating reviewers, and claiming preprints

## What This Does

Takes a video walkthrough (like a product demo or UI tour) and automatically generates:

1. **Linear Walkthrough** - Organized chapters with key takeaways and timestamps
2. **PRD Document** - Page-by-page specs for rebuilding the application  
3. **Personas & User Stories** - User-centric documentation with acceptance criteria

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
