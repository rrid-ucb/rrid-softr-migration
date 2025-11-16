#!/bin/bash
# Complete video annotation pipeline
# Usage: ./process_video.sh <video_file> [whisper_model] [llm_models]

set -e

VIDEO_FILE="${1}"
WHISPER_MODEL="${2:-base}"
LLM_MODELS="${3:-gemini openai}"

if [ -z "$VIDEO_FILE" ]; then
    echo "Usage: $0 <video_file> [whisper_model] [llm_models]"
    echo ""
    echo "Examples:"
    echo "  $0 design/softr.mp4"
    echo "  $0 design/softr.mp4 medium"
    echo "  $0 design/softr.mp4 medium 'gemini'"
    echo "  $0 design/softr.mp4 small 'gemini openai'"
    echo ""
    echo "Whisper models: tiny, base, small, medium, large"
    echo "LLM models: gemini, openai (space-separated)"
    exit 1
fi

if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: Video file not found: $VIDEO_FILE"
    exit 1
fi

# Extract base name without extension
BASENAME=$(basename "$VIDEO_FILE" .mp4)
BASENAME=$(basename "$BASENAME" .mov)
BASENAME=$(basename "$BASENAME" .avi)

echo "=================================================="
echo "Video Annotation Pipeline"
echo "=================================================="
echo "Video file: $VIDEO_FILE"
echo "Whisper model: $WHISPER_MODEL"
echo "LLM models: $LLM_MODELS"
echo "Output basename: $BASENAME"
echo "=================================================="
echo ""

# Step 1: Transcribe
echo "[1/4] Transcribing video with Whisper ($WHISPER_MODEL model)..."
whisper "$VIDEO_FILE" \
    --model "$WHISPER_MODEL" \
    --language en \
    --output_format json \
    --output_dir out

# Step 2: Extract frames
echo ""
echo "[2/4] Extracting key frames..."
mkdir -p out/frames
ffmpeg -hide_banner -i "$VIDEO_FILE" \
    -vf "select='gt(scene,0.30)',showinfo" \
    -vsync vfr out/frames/frame_%05d.jpg \
    2> out/frames/frames.log

# Step 3: Annotate
echo ""
echo "[3/4] Creating basic annotated transcript..."
python3 annotate_video.py \
    "$VIDEO_FILE" \
    "out/${BASENAME}.json" \
    out/frames \
    out/frames/frames.log \
    out

# Step 4: LLM processing
echo ""
echo "[4/4] Generating comprehensive documentation with LLMs..."
python3 llm_annotate.py out/annotated.json \
    --output-dir out/llm_docs \
    --models $LLM_MODELS

echo ""
echo "=================================================="
echo "✓ Pipeline complete!"
echo "=================================================="
echo ""
echo "Output files:"
echo "  Basic transcript:  out/annotated.md"
echo "  Full JSON:         out/annotated.json"
echo "  LLM docs:          out/llm_docs/"
echo ""
echo "View results:"
echo "  open out/annotated.md"
echo "  open out/llm_docs/README.md"
echo "=================================================="
