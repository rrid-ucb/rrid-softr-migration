# LLM-Powered Video Annotation System

Transform video walkthroughs into comprehensive product documentation using AI.

## Overview

This system takes a video walkthrough (e.g., a product demo or UI tour) and automatically generates three types of comprehensive documentation:

1. **Linear Walkthrough** - Chronological chapter/topic guide with key takeaways and timestamps
2. **PRD Document** - Page-by-page product requirements suitable for rebuilding the application
3. **Personas & User Stories** - User-centric documentation with journeys and acceptance criteria

## Quick Start

### 1. Install Dependencies

```bash
# Install system dependencies
brew install openai-whisper ffmpeg

# Install Python packages
pip install google-generativeai openai
```

### 2. Set API Keys

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
```

To make these permanent, add to your `~/.zshrc` or `~/.bashrc`:

```bash
echo 'export GEMINI_API_KEY="your_key"' >> ~/.zshrc
echo 'export OPENAI_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Process Your Video

```bash
# Step 1: Transcribe video with timestamps
whisper design/your-video.mp4 --model base --language en --output_format json --output_dir out

# Step 2: Extract key frames at scene changes
mkdir -p out/frames
ffmpeg -hide_banner -i design/your-video.mp4 \
  -vf "select='gt(scene,0.30)',showinfo" \
  -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Step 3: Create basic annotated transcript
python3 annotate_video.py design/your-video.mp4 out/your-video.json out/frames out/frames/frames.log out

# Step 4: Generate comprehensive LLM-powered documentation
python3 llm_annotate.py out/annotated.json --output-dir out/llm_docs --models gemini openai
```

## Output Structure

After running all steps, you'll have:

```
out/
├── annotated.json              # Timestamped transcript with frame references
├── annotated.md                # Basic markdown transcript
├── frames/                     # Extracted video frames
│   ├── frame_00001.jpg
│   ├── frame_00002.jpg
│   └── ...
├── llm_docs/                   # LLM-generated comprehensive docs
│   ├── README.md              # Comparison summary
│   ├── linear_walkthrough_gemini.md
│   ├── linear_walkthrough_openai.md
│   ├── prd_document_gemini.md
│   ├── prd_document_openai.md
│   ├── personas_stories_gemini.md
│   └── personas_stories_openai.md
└── your-video.json            # Raw Whisper transcript
```

## Document Types Explained

### 1. Linear Walkthrough
**Purpose:** Follow along with the video chronologically

**Contents:**
- Chapters organized by natural topic transitions
- Key takeaways for each section (3-5 bullets)
- Detailed descriptions of on-screen elements
- UI components, interactions, and workflows
- Referenced timestamps for key moments

**Use cases:**
- Understanding the application flow
- Training materials
- Feature overviews
- Documentation for existing users

### 2. PRD Document
**Purpose:** Rebuild the application from scratch

**Contents:**
- Executive summary
- Page-by-page breakdown
- UI components (buttons, forms, tables, menus)
- Features and functionality per page
- Business logic and validation rules
- Data models implied by the UI
- Technical requirements

**Use cases:**
- Development planning
- Feature specifications
- Competitive analysis
- Migration projects

### 3. Personas & User Stories
**Purpose:** Understand users and their needs

**Contents:**
- 3-5 user personas with backgrounds and goals
- User stories in standard format: "As a [persona], I want to [action] so that [benefit]"
- Acceptance criteria for each story
- Feature mapping to personas
- End-to-end user journeys
- Priority levels (High/Medium/Low)

**Use cases:**
- Product planning
- UX design
- Feature prioritization
- Stakeholder communication

## Advanced Usage

### Compare Multiple LLM Models

Generate documentation with both Gemini and OpenAI to compare quality:

```bash
python3 llm_annotate.py out/annotated.json --models gemini openai
```

This creates parallel versions of each document, allowing you to:
- Compare accuracy and detail level
- Choose the best output for each document type
- Combine insights from multiple models

### Use Only One Model

```bash
# Gemini only (faster, cost-effective)
python3 llm_annotate.py out/annotated.json --models gemini

# OpenAI only (may provide different perspectives)
python3 llm_annotate.py out/annotated.json --models openai
```

### Custom Output Directory

```bash
python3 llm_annotate.py out/annotated.json --output-dir docs/ai-generated
```

### Adjust Frame Extraction

Control how many frames are extracted:

```bash
# More frames (lower threshold = 0.20)
ffmpeg -hide_banner -i design/video.mp4 \
  -vf "select='gt(scene,0.20)',showinfo" \
  -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Fewer frames (higher threshold = 0.40)
ffmpeg -hide_banner -i design/video.mp4 \
  -vf "select='gt(scene,0.40)',showinfo" \
  -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Fixed interval (1 frame per second)
ffmpeg -hide_banner -i design/video.mp4 \
  -vf "fps=1,showinfo" \
  -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log
```

### Better Transcription Quality

Use larger Whisper models for better accuracy:

```bash
# Small model (good balance)
whisper design/video.mp4 --model small --language en --output_format json --output_dir out

# Medium model (better accuracy, slower)
whisper design/video.mp4 --model medium --language en --output_format json --output_dir out

# Large model (best quality, much slower)
whisper design/video.mp4 --model large --language en --output_format json --output_dir out
```

## API Keys

### Getting a Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as an environment variable

### Getting an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and set it as an environment variable

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"

```bash
export GEMINI_API_KEY="your_actual_key_here"
```

### "Warning: google-generativeai not installed"

```bash
pip install google-generativeai
```

### "Warning: openai not installed"

```bash
pip install openai
```

### Frames not matching transcript timing

This can happen if the video has variable frame rates. Try:
1. Extract more frames (lower scene threshold)
2. Use fixed interval extraction (`fps=1`)
3. Check that `frames.log` has pts_time entries

### Out of memory with large videos

1. Use a smaller Whisper model (`tiny` or `base`)
2. Process video in chunks
3. Reduce frame extraction rate

## Example Workflow: Complete Migration Project

Here's a full example for migrating an application:

```bash
# 1. Record a comprehensive walkthrough of the existing app
# (Use screen recording software like QuickTime, OBS, etc.)

# 2. Process the video
mkdir -p out/frames
whisper design/app-walkthrough.mp4 --model medium --language en --output_format json --output_dir out
ffmpeg -hide_banner -i design/app-walkthrough.mp4 -vf "select='gt(scene,0.30)',showinfo" -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log
python3 annotate_video.py design/app-walkthrough.mp4 out/app-walkthrough.json out/frames out/frames/frames.log out

# 3. Generate comprehensive documentation with both models
python3 llm_annotate.py out/annotated.json --output-dir out/migration_docs --models gemini openai

# 4. Review the outputs
open out/migration_docs/README.md

# 5. Use the documents:
# - Share PRD with development team
# - Use personas for product planning
# - Use linear walkthrough for training
```

## Tips for Best Results

### Recording the Video

1. **Speak clearly** - Describe what you're doing and what's on screen
2. **Go slowly** - Pause at important screens and features
3. **Show everything** - Navigate through all pages and features
4. **Explain context** - Mention user roles, workflows, and business logic
5. **Demo edge cases** - Show validation, errors, and special scenarios

### Optimizing Output Quality

1. **Better transcription** = better documentation
   - Use a quiet environment when recording
   - Speak clearly and at a moderate pace
   - Use the `medium` or `large` Whisper model

2. **More frames** = more visual context
   - Lower scene threshold for UI-heavy demos
   - Use fixed interval (`fps=1`) for consistent coverage

3. **Review and iterate**
   - Compare Gemini vs OpenAI outputs
   - Regenerate specific documents if needed
   - Edit the generated markdown for final polish

## Cost Considerations

- **Whisper**: Free (runs locally)
- **FFmpeg**: Free (runs locally)
- **Gemini API**: Check current pricing at https://ai.google.dev/pricing
- **OpenAI API**: Check current pricing at https://openai.com/pricing

Both APIs charge based on tokens (text + images). A typical 30-minute video might cost $1-5 to process with both models.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the generated `README.md` in your output directory
3. Verify API keys are set correctly
4. Check that all dependencies are installed

## License

This tool uses:
- OpenAI Whisper (MIT License)
- FFmpeg (GPL/LGPL)
- Google Generative AI Python SDK
- OpenAI Python SDK
