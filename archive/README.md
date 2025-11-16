# Archive

This directory contains legacy scripts and documentation that have been superseded by the new refactored system.

## Structure

- `legacy_scripts/` - Old Python scripts that have been refactored into the `src/` package
- `old_docs/` - Superseded documentation (currently empty)

## Legacy Scripts

These scripts are preserved for reference but are no longer actively maintained:

- `annotate_video.py` - Basic annotation (functionality moved to `src/video_processor/`)
- `llm_annotate.py` - LLM document generation (functionality moved to `src/llm/`)
- `extract_frames_from_timestamps.py` - Frame extraction (functionality moved to `src/frame_extraction/`)
- `extract_timestamp_frames.py` - Alternative frame extraction script
- `integrate_frames_into_docs.py` - Frame integration utility
- `generate_enriched_docs_with_vision.py` - Enhanced docs generation (needs integration into `src/llm/`)

## Migration

If you need functionality from these scripts, refer to:
- New system: `main.py` and `src/` package
- Documentation: `docs/REFACTORING_GUIDE.md` and `docs/MIGRATION_NOTES.md`

