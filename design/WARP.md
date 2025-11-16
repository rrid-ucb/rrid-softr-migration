# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a video annotation system that transforms video walkthroughs (e.g., product demos) into comprehensive AI-powered documentation. It was originally created to document a Softr application for migration, but can be used for any video-based documentation needs.

**Core Pipeline:**
1. Transcribe video using OpenAI Whisper (local)
2. Extract key frames using ffmpeg (scene detection)
3. Create timestamped transcript with frame annotations
4. Generate three types of comprehensive documents using LLMs (Gemini/OpenAI):
   - Linear walkthrough (chapters/topics with timestamps)
   - PRD document (page-by-page specifications)
   - Personas & user stories (user-centric documentation)

## Essential Commands

### First-Time Setup
```bash
# Install system dependencies (macOS)
brew install openai-whisper ffmpeg

# Create virtual environment and install packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set API keys (required for LLM processing)
export GEMINI_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

### Subsequent Sessions
```bash
# Always activate venv before running scripts
source venv/bin/activate
```

### Complete Pipeline
```bash
# Process video with all defaults (base Whisper model, both LLMs)
./process_video.sh design/video.mp4

# Custom options: whisper_model [tiny|base|small|medium|large]
./process_video.sh design/video.mp4 medium

# Custom LLM selection (space-separated: gemini, openai, or both)
./process_video.sh design/video.mp4 base gemini
./process_video.sh design/video.mp4 medium "gemini openai"
```

### Individual Steps
```bash
# Step 1: Transcribe
whisper design/video.mp4 --model base --language en --output_format json --output_dir out

# Step 2: Extract frames (scene detection threshold 0.30)
mkdir -p out/frames
ffmpeg -hide_banner -i design/video.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Step 3: Create basic annotation
python3 annotate_video.py design/video.mp4 out/video.json out/frames out/frames/frames.log out

# Step 4: Generate LLM documentation
python3 llm_annotate.py out/annotated.json --models gemini openai
```

### Testing & Diagnostics
```bash
# Check system setup and dependencies
./setup_and_test.sh

# Regenerate LLM docs from existing annotated.json
./run_llm_docs.sh
```

## Architecture

### Script Responsibilities

**annotate_video.py** - Basic annotation script
- Loads Whisper transcript JSON (handles multiple format variations)
- Parses frame extraction log to get pts_time for each frame
- Matches transcript segments to nearest frame within time window
- Outputs `annotated.json` (machine-readable) and `annotated.md` (human-readable)

**llm_annotate.py** - LLM-powered documentation generator
- `VideoAnnotationProcessor` class manages the entire workflow
- Prepares transcript context with timestamps and frame references
- Calls Gemini (gemini-2.0-flash-exp) and/or OpenAI (gpt-4o) APIs
- Images sent to Gemini via `genai.upload_file()`, to OpenAI as base64
- Generates three document types using distinct prompts:
  - `generate_linear_walkthrough()` - Chronological chapters
  - `generate_prd_document()` - Page-by-page specifications
  - `generate_personas_stories()` - User personas and stories
- Creates comparison README when multiple models used

**process_video.sh** - All-in-one pipeline orchestrator
- Activates venv automatically if present
- Runs all four steps in sequence
- Configurable Whisper model and LLM selection
- Provides progress feedback and final output summary

### Data Flow

```
video.mp4 
  → Whisper → video.json (raw transcript)
  → ffmpeg → frames/*.jpg + frames.log (pts_time data)
  → annotate_video.py → annotated.json + annotated.md
  → llm_annotate.py → llm_docs/*.md (3 doc types × N models)
```

### Key Design Decisions

**Frame Matching Logic** (`annotate_video.py:nearest_frame()`):
- Prefers frames whose timestamp falls within segment's [start, end] window
- Falls back to nearest frame to segment start if no frame in window
- This handles variable scene detection vs. fixed transcript segments

**LLM Context Preparation**:
- Full transcript always included as text context
- Frames sampled at intervals (default every 5th or 8th item) to manage API limits
- Frame paths made absolute before passing to APIs
- Each model gets identical input for fair comparison

**Output Organization**:
- Basic output in `out/` directory: `annotated.{json,md}`, `frames/`
- LLM docs isolated in `out/llm_docs/` subdirectory
- Each document type has model-specific versions: `*_gemini.md`, `*_openai.md`
- Allows comparing model outputs side-by-side

## Development Guidelines

### Adding New LLM Providers
- Add API client setup in `VideoAnnotationProcessor.__init__()`
- Create call method following pattern of `call_gemini()` / `call_openai()`
- Handle both text-only and multimodal (image) contexts
- Update model selection in argument parser

### Modifying Document Types
- Each document type has dedicated `generate_*()` method
- Prompts are inline strings for easy iteration
- Adjust frame sampling rate per document type needs
- Consider token limits when adding more context

### Frame Extraction Tuning
- Scene threshold: lower (0.20) = more frames, higher (0.40) = fewer frames
- Alternative: fixed interval with `fps=1` filter
- Frame extraction log must be preserved for pts_time parsing

### Testing Without API Keys
- Steps 1-3 work without API keys (local Whisper + ffmpeg + annotation)
- Step 4 requires at least one API key (Gemini or OpenAI)
- Use `setup_and_test.sh` to validate environment before processing

## File Structure

```
.
├── annotate_video.py          # Step 3: Match transcript to frames
├── llm_annotate.py            # Step 4: Generate LLM docs
├── process_video.sh           # All-in-one pipeline
├── run_llm_docs.sh           # Regenerate docs from existing annotated.json
├── setup_and_test.sh         # Environment verification
├── requirements.txt           # Python deps: google-generativeai, openai
├── design/                    # Input videos go here
├── out/                       # Generated output
│   ├── annotated.json         # Timestamped transcript data
│   ├── annotated.md          # Human-readable transcript
│   ├── frames/               # Extracted screenshots
│   └── llm_docs/             # AI-generated documents
└── venv/                      # Virtual environment (created by setup)
```

## Common Issues

**"GEMINI_API_KEY not set"** - Export the environment variable before running step 4
**"No module named 'google'"** - Virtual environment not activated: `source venv/bin/activate`
**Poor transcription quality** - Use larger Whisper model: `medium` or `large` instead of `base`
**Frames not matching segments well** - Adjust scene detection threshold or use fixed interval extraction
**"Could not find segments in transcript JSON"** - Whisper output format changed; update `load_segments()` parser

## API Information

**API Keys:**
- Gemini: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

**Models Used:**
- Gemini: `gemini-2.0-flash-exp` (vision model, supports image uploads)
- OpenAI: `gpt-4o` (vision model, supports base64 images)

**Typical Costs:**
- Whisper: Free (runs locally)
- Gemini: ~$0.50-2.00 per 30-minute video
- OpenAI: ~$1.00-3.00 per 30-minute video
