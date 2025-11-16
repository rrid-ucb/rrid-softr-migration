# Usage Examples

## Example 1: Process Your Existing Video

You already have `design/softr.mp4` processed. Generate LLM documentation:

```bash
# With Gemini only (recommended to start)
python3 llm_annotate.py out/annotated.json --models gemini

# With both models for comparison
python3 llm_annotate.py out/annotated.json --models gemini openai
```

## Example 2: Full Pipeline on New Video

```bash
./process_video.sh design/new-video.mp4
```

## Example 3: High Quality Processing

```bash
# Step 1: Better transcription with medium model
whisper design/softr.mp4 --model medium --language en --output_format json --output_dir out

# Step 2: More frames (lower threshold)
mkdir -p out/frames
ffmpeg -hide_banner -i design/softr.mp4 \
  -vf "select='gt(scene,0.20)',showinfo" \
  -vsync vfr out/frames/frame_%05d.jpg 2> out/frames/frames.log

# Step 3: Re-annotate
python3 annotate_video.py design/softr.mp4 out/softr.json out/frames out/frames/frames.log out

# Step 4: Generate docs with both models
python3 llm_annotate.py out/annotated.json --models gemini openai --output-dir out/high_quality_docs
```

## Example 4: Quick Test with Existing Data

Since you already have `out/annotated.json`, you can test the LLM generation right now:

```bash
# Make sure API keys are set
echo "Checking API keys..."
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:0:10}..."
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."

# Install Python packages if needed
pip install google-generativeai openai

# Generate docs with Gemini (faster)
python3 llm_annotate.py out/annotated.json --models gemini --output-dir out/test_gemini

# Check the output
ls -lh out/test_gemini/
```

## What You'll Get

After running LLM processing, you'll have:

```
out/llm_docs/
├── README.md                          # Overview and comparison
├── linear_walkthrough_gemini.md       # Chronological guide
├── prd_document_gemini.md             # Page-by-page specs
└── personas_stories_gemini.md         # User stories
```

If you ran with both models:
```
out/llm_docs/
├── README.md
├── linear_walkthrough_gemini.md       # Gemini's version
├── linear_walkthrough_openai.md       # OpenAI's version  
├── prd_document_gemini.md
├── prd_document_openai.md
├── personas_stories_gemini.md
└── personas_stories_openai.md
```

## Document Contents Preview

### linear_walkthrough_*.md
- Chapters organized by natural topic breaks
- Key takeaways (3-5 bullets per section)
- Detailed UI descriptions
- Referenced timestamps [HH:MM:SS]
- Screenshots at key moments

### prd_document_*.md
- Executive summary
- Table of contents
- Page-by-page breakdown:
  - Page purpose and navigation
  - Visual layout
  - UI components (buttons, forms, tables)
  - Features and functionality
  - Business logic and validation
  - Data models

### personas_stories_*.md
- 3-5 user personas with:
  - Background and goals
  - Pain points
  - Technical skill level
- User stories: "As a [persona], I want to [action] so that [benefit]"
- Acceptance criteria
- Feature mapping to personas
- End-to-end user journeys

## Real-World Workflow

### Migration Project (Your Use Case)

```bash
# 1. You've already done this:
#    - Recorded softr.mp4
#    - Transcribed it
#    - Extracted frames

# 2. Generate comprehensive docs for migration
python3 llm_annotate.py out/annotated.json --models gemini openai

# 3. Share with team
open out/llm_docs/prd_document_gemini.md          # For developers
open out/llm_docs/personas_stories_gemini.md      # For product managers
open out/llm_docs/linear_walkthrough_gemini.md    # For everyone

# 4. Compare Gemini vs OpenAI outputs
diff out/llm_docs/prd_document_gemini.md out/llm_docs/prd_document_openai.md

# 5. Use in your migration planning
```

## Tips

1. **Start with Gemini only** - It's faster and cheaper, good for initial review
2. **Add OpenAI for comparison** - Different models notice different things
3. **Edit the output** - The generated docs are starting points, refine them
4. **Iterate** - If you miss something, record a follow-up video and process it

## Next Steps

Ready to try it? Run:

```bash
# Check your setup
./setup_and_test.sh

# Process your existing data
python3 llm_annotate.py out/annotated.json --models gemini
```

Then open `out/llm_docs/` to see your comprehensive documentation!
