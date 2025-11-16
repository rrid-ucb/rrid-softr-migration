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

## One-Line Command

```bash
./process_video.sh design/your-video.mp4
```

This will:
1. Transcribe the video with Whisper
2. Extract key frames
3. Create annotated transcript
4. Generate 3 comprehensive documents with both Gemini and OpenAI

## Manual Steps

### Step 1: Transcribe
```bash
whisper design/video.mp4 --model base --language en --output_format json --output_dir out
```

### Step 2: Extract frames
```bash
mkdir -p out/frames
ffmpeg -hide_banner -i design/video.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log
```

### Step 3: Basic annotation
```bash
python3 annotate_video.py design/video.mp4 out/video.json out/frames out/frames/frames.log out
```

### Step 4: LLM-powered docs
```bash
# Both models (recommended for comparison)
python3 llm_annotate.py out/annotated.json --models gemini openai

# Single model
python3 llm_annotate.py out/annotated.json --models gemini
```

## Output Files

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

```bash
# Better transcription quality
./process_video.sh design/video.mp4 medium

# Use only Gemini (faster/cheaper)
./process_video.sh design/video.mp4 base gemini

# Best quality
./process_video.sh design/video.mp4 large "gemini openai"
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

## Full Documentation

See `LLM_ANNOTATION_README.md` for complete details.
