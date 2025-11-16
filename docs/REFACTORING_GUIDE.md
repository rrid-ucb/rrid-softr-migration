# Refactoring Guide - New Structure

## Overview

The codebase has been refactored into a modular structure with improved organization, configuration management, and enhanced features.

## New Directory Structure

```
.
├── src/                          # Source code (Python modules)
│   ├── config/                   # Configuration management
│   │   ├── models.py             # Model discovery and selection
│   │   └── manager.py            # Configuration manager
│   ├── metadata/                 # Video metadata extraction
│   │   └── extractor.py          # EXIF, video properties, creation time
│   ├── frame_extraction/         # Enhanced frame extraction
│   │   └── extractor.py          # Blank frame detection, audio analysis
│   ├── transcription/            # Transcription (Whisper integration)
│   ├── llm/                      # LLM integration (Gemini/OpenAI)
│   └── video_processor/          # Main pipeline orchestration
│       └── pipeline.py            # Complete video processing pipeline
├── input/                        # Input videos directory
├── output/                       # Output directory (timestamped runs)
│   └── {video_name}/
│       └── {timestamp}/
│           ├── metadata.json     # Video metadata
│           ├── {video}.json      # Transcript
│           ├── annotated.json    # Annotated transcript
│           ├── frames/           # Extracted frames
│           └── llm_docs/         # Generated documentation
├── config/                       # Configuration files (gitignored)
├── main.py                       # Main entry point
└── requirements.txt              # Dependencies
```

## Key Improvements

### 1. Configuration System
- **Dynamic Model Discovery**: Automatically queries APIs for available models
- **First-Run Configuration**: Interactive setup with model selection
- **Speed Preferences**: Choose fast/balanced/accurate for each task type
- **Runtime Overrides**: Command-line args to override configuration

### 2. Enhanced Frame Extraction
- **Blank Frame Detection**: Automatically skips black/blank frames
- **Audio Analysis**: Prioritizes frames with audio activity
- **Transcript Heuristics**: Uses transcript to guide frame selection
- **Better Alignment**: Frames aligned with actual content

### 3. Metadata Extraction
- **Video Properties**: Resolution, duration, codec, bitrate
- **Creation Time**: Extracts from EXIF/metadata
- **Audio Info**: Codec, sample rate, channels
- **Saved as JSON**: All metadata preserved for reference

### 4. Timestamped Outputs
- Each video run gets its own timestamped directory
- Easy to track multiple processing runs
- All artifacts organized per video

### 5. Multi-Video Support
- Process single video or entire directory
- Each video gets its own output directory
- Batch processing with progress tracking

## Usage

### First-Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure system (interactive)
python main.py --configure
```

### Process Videos

```bash
# Process single video
python main.py --process input/video.mp4

# Process all videos in directory
python main.py --process-all input/

# Process without timestamped directories
python main.py --process input/video.mp4 --no-timestamp
```

### List Available Models

```bash
python main.py --list-models
```

### Reconfigure

```bash
python main.py --configure
```

## Migration from Old Structure

The old scripts still work, but the new structure provides:

1. **Better Organization**: Modular code, easier to maintain
2. **Configuration Management**: No more hard-coded models
3. **Enhanced Features**: Blank frame detection, audio analysis
4. **Better Outputs**: Timestamped directories, metadata preservation

## Configuration File Location

Configuration is stored in: `~/.video_annotation/config.json`

You can override with `--config-dir` option.

## Model Selection Rubric

The system uses the following rubric for model selection:

- **Transcription**: Whisper models (tiny/base/small/medium/large)
  - Fast: tiny, base
  - Balanced: base, small
  - Accurate: medium, large, large-v3

- **Vision**: Gemini Vision or GPT-4 Vision
  - Fast: Gemini Flash
  - Balanced: Gemini Pro Vision, GPT-4o
  - Accurate: GPT-4 Vision

- **General**: GPT-4, Gemini Pro
  - Fast: GPT-4 Turbo, Gemini Flash
  - Balanced: GPT-4, Gemini Pro
  - Accurate: GPT-4, Gemini Pro

- **Thinking**: O1 models (if available)
  - For complex reasoning tasks

## Output Structure Example

```
output/
└── softr/
    └── 20250115_143022/          # Timestamped run
        ├── metadata.json          # Video metadata
        ├── softr.json             # Whisper transcript
        ├── annotated.json         # Annotated transcript
        ├── frames/
        │   ├── frame_00001_00-00.jpg
        │   ├── frames_timestamps.json
        │   └── frames_timestamps.csv
        └── llm_docs/
            ├── linear_walkthrough_enriched.md
            ├── prd_document_enriched.md
            └── personas_stories_enriched.md
```

