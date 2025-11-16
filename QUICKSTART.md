# Quick Start Guide

## Prerequisites

```bash
# Install system dependencies
brew install openai-whisper ffmpeg

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Set API keys (required for LLM step)
export GEMINI_API_KEY="your_gemini_key"
export OPENAI_API_KEY="your_openai_key"
```

**For subsequent sessions, just activate venv:**
```bash
source venv/bin/activate
```

## New Refactored System (Recommended)

### First-Time Setup

```bash
# Configure system (interactive - run in your terminal)
python main.py --configure
```

The configuration will:
- Discover available models from your API keys
- Let you choose models for each task type (transcription, vision, general, thinking)
- Set speed preferences (fast/balanced/accurate)
- Save configuration to `~/.video_annotation/config.json`

### Process Videos

```bash
# Process single video
python main.py --process input/video.mp4

# Process all videos in input directory
python main.py --process-all input/

# Process without timestamped directories
python main.py --process input/video.mp4 --no-timestamp
```

### Output Structure (New System)

Each video gets its own directory with timestamped runs:

```
output/
└── {video_name}/
    └── {YYYYMMDD_HHMMSS}/     # Timestamped run
        ├── metadata.json       # Video metadata (EXIF, properties, creation time)
        ├── {video}.json        # Whisper transcript
        ├── annotated.json      # Annotated transcript with frames
        ├── frames/            # Extracted frames (with blank detection)
        │   ├── frame_00001_00-00.jpg
        │   ├── frames_timestamps.json
        │   └── frames_timestamps.csv
        └── llm_docs/          # Generated documentation
            ├── linear_walkthrough.md
            ├── prd_document.md
            └── personas_stories.md
```

### Features (New System)

- ✅ **Blank Frame Detection**: Automatically skips black/blank frames
- ✅ **Audio Analysis**: Prioritizes frames with audio activity  
- ✅ **Metadata Extraction**: Captures video properties and creation time
- ✅ **Dynamic Model Selection**: Automatically discovers and selects best models
- ✅ **Timestamped Outputs**: Each run gets its own directory
- ✅ **Multi-Video Support**: Process entire directories

### Reconfigure Anytime

```bash
python main.py --configure
```

### List Available Models

```bash
python main.py --list-models
```

## Legacy System (Still Supported)

The old scripts still work if you prefer the original workflow:

```bash
# One-line command
./scripts/process_video.sh input/your-video.mp4

# This will:
# 1. Transcribe the video with Whisper
# 2. Extract key frames
# 3. Create annotated transcript
# 4. Generate 3 comprehensive documents with both Gemini and OpenAI
```

### Manual Steps (Legacy)

```bash
# Step 1: Transcribe
whisper design/video.mp4 --model base --language en --output_format json --output_dir out

# Step 2: Extract frames
mkdir -p out/frames
ffmpeg -hide_banner -i design/video.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Step 3: Basic annotation
python3 archive/legacy_scripts/annotate_video.py input/video.mp4 out/video.json out/frames out/frames/frames.log out

# Step 4: LLM-powered docs
python3 archive/legacy_scripts/llm_annotate.py out/annotated.json --models gemini openai
```

### Legacy Output Structure

```
out/
├── annotated.md                           # Basic timestamped transcript
├── annotated.json                         # Machine-readable data
└── llm_docs/                              # AI-generated documentation
    ├── README.md                          # Overview
    ├── linear_walkthrough_gemini.md       # Chapter/topic walkthrough
    ├── linear_walkthrough_openai.md       # (OpenAI version)
    ├── prd_document_gemini.md             # Page-by-page PRD
    ├── prd_document_openai.md             # (OpenAI version)
    ├── personas_stories_gemini.md         # User personas & stories
    └── personas_stories_openai.md         # (OpenAI version)
```

## Document Types

1. **Linear Walkthrough** → Training, documentation, feature overview
2. **PRD Document** → Development planning, migration specs
3. **Personas & User Stories** → Product planning, UX design, prioritization

## Common Options

### New System

```bash
# Process with custom output directory
python main.py --process input/video.mp4 --output-dir custom_output/

# Process all videos in directory
python main.py --process-all input/
```

### Legacy System

```bash
# Better transcription quality
./scripts/process_video.sh input/video.mp4 medium

# Use only Gemini (faster/cheaper)
./scripts/process_video.sh input/video.mp4 base gemini

# Best quality
./scripts/process_video.sh input/video.mp4 large "gemini openai"
```

## Troubleshooting

**"GEMINI_API_KEY not set"**
```bash
export GEMINI_API_KEY="your_key_here"
```

**Need API keys?**
- Gemini: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

**Missing packages?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Virtual environment not activated?**
```bash
source venv/bin/activate
```

**Configuration issues?**
```bash
# Reconfigure the system
python main.py --configure

# Or check available models
python main.py --list-models
```

## Full Documentation

- **New System**: See `REFACTORING_GUIDE.md` and `MIGRATION_NOTES.md`
- **Legacy System**: See `LLM_ANNOTATION_README.md` for complete details

## Which System Should I Use?

- **Use New System** (`main.py`) if you want:
  - Better organization with timestamped outputs
  - Automatic blank frame detection
  - Audio analysis for better frame selection
  - Dynamic model discovery and configuration
  - Multi-video batch processing

- **Use Legacy System** (`process_video.sh`) if you want:
  - Simple one-command processing
  - Familiar workflow
  - Direct control over Whisper models

Both systems produce the same quality outputs and can be used interchangeably.
