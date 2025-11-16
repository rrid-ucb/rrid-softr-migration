# Migration Notes

## What's New

The codebase has been refactored with the following improvements:

### ✅ Completed

1. **New Directory Structure**
   - `src/` - Modular Python package
   - `output/` - Timestamped output directories
   - `config/` - Configuration management

2. **Configuration System**
   - Dynamic model discovery
   - First-run configuration
   - Speed preferences (fast/balanced/accurate)

3. **Metadata Extraction**
   - Video properties (resolution, duration, codec)
   - Creation time from EXIF
   - Audio information

4. **Enhanced Frame Extraction**
   - Blank frame detection
   - Audio activity analysis
   - Better frame selection

5. **Main Entry Point**
   - `main.py` with CLI interface
   - `--configure` option
   - `--process` and `--process-all` options

### 🔄 Partially Integrated

The LLM generation logic from `llm_annotate.py` and `generate_enriched_docs_with_vision.py` needs to be fully integrated into the new `src/llm/generator.py` module. The structure is in place but the actual generation methods are placeholders.

### 📝 Next Steps

1. **Full LLM Integration**: Move complete logic from old scripts to new modules
2. **Test Configuration**: Run `python main.py --configure`
3. **Test Processing**: Process a video with new structure
4. **Migrate Existing Data**: Optionally migrate old `out/` structure

## Backward Compatibility

The old scripts (`process_video.sh`, `llm_annotate.py`, etc.) still work and are preserved. The new system is additive - you can use either approach.

## Quick Start with New Structure

```bash
# 1. Configure (first time)
python main.py --configure

# 2. Process video
python main.py --process input/video.mp4

# 3. Process all videos
python main.py --process-all input/
```

