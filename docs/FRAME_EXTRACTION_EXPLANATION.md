# Frame Extraction System Explanation

## How the Codebase Works

### 1. Video Processing Pipeline (`process_video.sh`)

The pipeline has 4 main steps:

1. **Transcription** - Uses OpenAI Whisper to transcribe the video with timestamps
2. **Frame Extraction** - Uses ffmpeg to extract key frames at scene changes
3. **Annotation** - Matches transcript segments with extracted frames
4. **LLM Processing** - Generates comprehensive documentation using AI

### 2. Why So Few Frames?

The current frame extraction uses **scene detection** with a threshold:

```bash
ffmpeg -vf "select='gt(scene,0.30)',showinfo" ...
```

This only extracts frames when there's a **significant visual change** (scene change score > 0.30). For a ~22 minute video, this resulted in only **6 frames**:
- Frame 1: 0.96s
- Frame 2: 848.04s (~14:08)
- Frame 3: 849.24s (~14:09)
- Frame 4: 874.96s (~14:35)
- Frame 5: 875.36s (~14:35)
- Frame 6: 1239.76s (~20:40)

**Problem**: The LLM-generated markdown files reference many more timestamps (00:00, 00:40, 00:47, 01:06, 02:14, 03:11, 05:04, 07:08, 13:32, 14:09, 18:34, 20:21, 21:37, etc.) that don't have corresponding frames.

### 3. Current Screenshot Embedding (`llm_annotate.py`)

The `embed_screenshots_in_markdown()` method:
- Parses timestamps from markdown (e.g., `[00:47]`)
- Tries to find the closest existing frame within 30 seconds
- Since there are so few frames, many timestamps can't find matches

### 4. Solution: Extract Frames at Specific Timestamps

The new `extract_timestamp_frames.py` script:

1. **Scans markdown files** for all timestamp references (e.g., `[00:47]`, `[01:06]`)
2. **Extracts frames** at those exact timestamps using ffmpeg
3. **Updates markdown files** to reference the newly extracted frames

## Usage

```bash
# Extract frames for all timestamps referenced in markdown files
python3 extract_timestamp_frames.py \
    design/softr.mp4 \
    out/annotated.json \
    out/llm_docs
```

This will:
- Find all timestamps in `out/llm_docs/*.md` files
- Extract frames at those timestamps to `out/frames/`
- Update the markdown files to include screenshot references

## Timestamp Format

The script recognizes timestamps in formats:
- `[MM:SS]` - e.g., `[00:47]`, `[01:06]`
- `[HH:MM:SS]` - e.g., `[00:01:36]`, `[00:14:09]`

Found in patterns like:
- `**[00:47]** - Explanation of...`
- `- **[01:06]** - Introduction of...`
- `1. **[00:47] Landing Page:** ...`

## Frame Extraction Method

Uses ffmpeg's `-ss` (seek) option to extract frames at exact timestamps:

```bash
ffmpeg -ss <timestamp_seconds> -i <video> -vframes 1 -q:v 2 <output.jpg>
```

This is more precise than scene detection and ensures we get frames at the exact moments referenced in the documentation.

