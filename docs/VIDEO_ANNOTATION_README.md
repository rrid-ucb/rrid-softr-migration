# Video Transcription & Annotation

This workflow transcribes MP4 videos with timestamps and extracts key frames at scene changes, producing machine-readable JSON and human-readable Markdown.

## Installation

```bash
brew install openai-whisper ffmpeg
```

## Usage

### 1. Transcribe video
```bash
whisper design/softr.mp4 --model base --language en --output_format json --output_dir out
```

**Model options:** `tiny`, `base`, `small`, `medium`, `large` (larger = better quality, slower)

### 2. Extract key frames at scene changes
```bash
ffmpeg -hide_banner -i design/softr.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log
```

**Tuning:**
- Lower threshold (`0.20`) = more frames
- Higher threshold (`0.40`) = fewer frames
- Fixed interval: replace `select='gt(scene,0.30)'` with `fps=1` for 1 frame/sec

### 3. Generate annotated output
```bash
python3 annotate_video.py design/softr.mp4 out/softr.json out/frames out/frames/frames.log out
```

## Output

- **`out/annotated.json`** — Machine-readable JSON with transcript segments, timestamps, and matched frames
- **`out/annotated.md`** — Human-readable Markdown with screenshots and timestamps (images use relative path `frames/`)
- **`out/frames/frame_*.jpg`** — Extracted key frames

## JSON Structure

```json
{
  "video": "design/softr.mp4",
  "transcript": "out/softr.json",
  "frames_dir": "frames",
  "items": [
    {
      "id": 0,
      "start": 0.0,
      "end": 10.24,
      "start_hms": "00:00",
      "end_hms": "00:10",
      "text": "Awesome. Okay, so this is going to be...",
      "frame": {
        "path": "frames/frame_00001.jpg",
        "time": 0.96
      }
    }
  ]
}
```

## Example Run

```bash
# For design/softr.mp4
mkdir -p out/frames
whisper design/softr.mp4 --model base --language en --output_format json --output_dir out
ffmpeg -hide_banner -i design/softr.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log
python3 annotate_video.py design/softr.mp4 out/softr.json out/frames out/frames/frames.log out
open out/annotated.md
```
