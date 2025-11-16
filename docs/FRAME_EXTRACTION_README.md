# Frame Extraction and Screenshot Update Guide

## Problem

The original frame extraction in `process_video.sh` uses scene detection with a threshold of 0.30, which only captures major scene changes. This results in very few frames (e.g., only 6 frames for a 22-minute video) even though there are 168 transcript segments.

## Solution

The `extract_frames_from_timestamps.py` script:

1. **Parses timestamps** from LLM-generated markdown documentation files
2. **Extracts frames** from the video at those exact timestamps
3. **Updates markdown files** with correct screenshot references

## How It Works

### 1. Timestamp Extraction

The script finds all timestamp references in markdown files using the pattern `[HH:MM]` or `[HH:MM:SS]`. Examples:
- `[00:00]` - Introduction
- `[01:23]` - Landing page explanation
- `[13:32]` - Quality check portal

### 2. Frame Extraction

For each unique timestamp:
- Converts timestamp string to seconds
- Uses `ffmpeg` to extract a frame at that exact time
- Saves frames as `frame_00001.jpg`, `frame_00002.jpg`, etc.
- Avoids duplicates (if timestamps are within 0.5 seconds, reuses the same frame)

### 3. Markdown Update

The script updates markdown files to include screenshot references:
- Finds lines with timestamp references
- Checks if screenshot already exists (to avoid duplicates)
- Adds `![Screenshot at HH:MM](../frames/frame_XXXXX.jpg)` below the timestamp

## Usage

### Basic Usage (Extract frames for timestamps in markdown docs)

```bash
python3 extract_frames_from_timestamps.py design/softr.mp4
```

This will:
- Parse timestamps from `out/llm_docs/*.md` files
- Extract frames at those timestamps
- Update the markdown files with screenshot references

### Extract Frames for All Transcript Segments

```bash
python3 extract_frames_from_timestamps.py design/softr.mp4 --extract-all-segments
```

This will extract frames for:
- All timestamps referenced in markdown docs
- **Plus** all 168 transcript segment timestamps

This ensures you have screenshots for every part of the video, not just the ones mentioned in the docs.

### Custom Paths

```bash
python3 extract_frames_from_timestamps.py \
    design/softr.mp4 \
    --annotated-json out/annotated.json \
    --frames-dir out/frames \
    --llm-docs-dir out/llm_docs
```

## Understanding the Codebase

### Frame Extraction Pipeline

1. **`process_video.sh`** - Main pipeline script
   - Transcribes video with Whisper
   - Extracts frames using scene detection (limited!)
   - Creates annotated.json
   - Generates LLM docs

2. **`annotate_video.py`** - Basic annotation
   - Loads transcript segments
   - Matches frames to transcript timestamps
   - Creates `annotated.json` and `annotated.md`

3. **`llm_annotate.py`** - LLM documentation generation
   - Uses Gemini/OpenAI to generate docs
   - Has `embed_screenshots_in_markdown()` method that tries to add screenshots
   - But it's limited because there are so few frames!

4. **`extract_frames_from_timestamps.py`** - NEW! Enhanced frame extraction
   - Extracts frames at specific timestamps
   - Updates markdown files with correct references

### Why So Few Frames?

The original `process_video.sh` uses:
```bash
ffmpeg -vf "select='gt(scene,0.30)'" ...
```

This only extracts frames when the scene change score is > 0.30. For a screen recording with gradual changes, this results in very few frames.

### Solution: Extract at Timestamps

Instead of relying on scene detection, we extract frames at:
- **Specific timestamps** mentioned in the documentation
- **All transcript segment start times** (if using `--extract-all-segments`)

This ensures we have screenshots exactly where they're needed.

## Example Workflow

### Step 1: Initial Processing (if not done)

```bash
./process_video.sh design/softr.mp4
```

This creates:
- `out/annotated.json` - Transcript with timestamps
- `out/llm_docs/*.md` - Generated documentation
- `out/frames/frame_*.jpg` - Few frames (scene detection)

### Step 2: Extract More Frames

```bash
python3 extract_frames_from_timestamps.py design/softr.mp4 --extract-all-segments
```

This:
- Extracts frames at all timestamps mentioned in docs
- Extracts frames for all 168 transcript segments
- Updates markdown files with screenshot references

### Step 3: Review Results

```bash
# Check how many frames were extracted
ls -1 out/frames/frame_*.jpg | wc -l

# View updated markdown
open out/llm_docs/linear_walkthrough_openai.md
```

## Timestamp Format

The script handles both formats:
- `[00:47]` - Minutes:Seconds (most common in docs)
- `[01:23:45]` - Hours:Minutes:Seconds

## Troubleshooting

### "No frames extracted"

- Check that video file exists and is readable
- Verify `ffmpeg` is installed: `which ffmpeg`
- Check video duration: `ffprobe design/softr.mp4`

### "Timestamps not found in markdown"

- Verify markdown files exist in `out/llm_docs/`
- Check that timestamps are in format `[HH:MM]` or `[HH:MM:SS]`
- Run with `--extract-all-segments` to use transcript timestamps

### "Screenshots not showing in markdown"

- Check relative paths: markdown files should reference `../frames/`
- Verify frame files exist: `ls out/frames/frame_*.jpg`
- Check markdown syntax: images should be `![alt](path)`

## Integration with Existing Code

The `llm_annotate.py` script already has an `embed_screenshots_in_markdown()` method, but it's limited because:
1. It only finds frames that already exist
2. It uses a 30-second threshold to find "close" frames
3. With only 6 frames, most timestamps don't have close matches

The new script solves this by:
1. Extracting frames at the exact timestamps needed
2. Ensuring frames exist for all referenced timestamps
3. Updating markdown files with correct references

## Future Improvements

- Cache extracted frames to avoid re-extraction
- Support extracting frames at regular intervals (e.g., every 10 seconds)
- Better duplicate detection (currently 0.5 second threshold)
- Batch processing for multiple videos

