# Output Directory Structure

This directory contains run-based outputs organized by video and timestamp.

## Structure

```
output/
└── {video_name}/              # Video name (e.g., softr)
    └── {run_timestamp}/       # Run timestamp (YYYYMMDD_HHMMSS)
        ├── run_metadata.json  # Run metadata and file counts
        ├── frames/            # Extracted video frames
        │   ├── frame_*.jpg
        │   ├── frames_timestamps.json
        │   └── frames_timestamps.csv
        ├── transcripts/       # Transcripts and annotations
        │   ├── {video}.json   # Whisper transcript
        │   ├── annotated.json # Annotated transcript
        │   └── annotated.md   # Human-readable transcript
        └── docs/              # Generated documentation
            ├── {model}/       # Model-specific docs (e.g., openai, gemini_vision)
            │   ├── linear_walkthrough.md
            │   ├── prd_document.md
            │   └── personas_stories.md
            └── ...
```

## Example

```
output/
└── softr/
    ├── 20251115_225000/       # Initial transcription run
    │   ├── transcripts/
    │   │   ├── softr.json
    │   │   └── annotated.json
    │   └── docs/
    │       └── unknown/
    │           └── annotated.md
    │
    ├── 20251116_002000/       # Frame extraction run
    │   ├── frames/
    │   │   ├── frame_00001_00-00.jpg
    │   │   └── ...
    │   └── run_metadata.json
    │
    ├── 20251116_003000/       # OpenAI docs generation
    │   └── docs/
    │       └── openai/
    │           ├── linear_walkthrough.md
    │           ├── prd_document.md
    │           └── personas_stories.md
    │
    └── 20251116_010000/       # Gemini Vision docs generation
        └── docs/
            └── gemini_vision/
                ├── linear_walkthrough.md
                ├── prd_document.md
                └── personas_stories.md
```

## Model Variants

Documentation is organized by model/provider:
- `openai` - OpenAI GPT models
- `gemini` - Google Gemini models
- `gemini_vision` - Gemini Vision models (previously called "enriched")
- `unknown` - Unspecified or mixed sources

## Run Metadata

Each run includes `run_metadata.json` with:
- Run timestamp
- Video name
- File counts by category
- Model variants used

## Notes

- Each run is timestamped for easy tracking
- Multiple runs can exist for the same video (different configurations)
- Frames are shared across runs when extracted at the same time
- Documentation is separated by model for easy comparison

