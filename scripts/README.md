# Utility Scripts

This directory contains utility scripts for the video annotation system.

## Scripts

### `process_video.sh`
Legacy all-in-one pipeline script. Processes a video through all steps:
- Transcription with Whisper
- Frame extraction
- Annotation
- LLM document generation

**Usage:**
```bash
./scripts/process_video.sh input/video.mp4 [whisper_model] [llm_models]
```

### `run_llm_docs.sh`
Regenerate LLM documentation from existing `annotated.json`.

**Usage:**
```bash
./scripts/run_llm_docs.sh
```

### `setup_and_test.sh`
Environment verification and testing script.

**Usage:**
```bash
./scripts/setup_and_test.sh
```

## Note

These scripts are part of the legacy system. The new refactored system uses `main.py` as the entry point. These scripts are preserved for backward compatibility.

