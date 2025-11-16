# RRID Softr Migration - Video Annotation System

Transform video walkthroughs into comprehensive product documentation using AI-powered analysis.

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
