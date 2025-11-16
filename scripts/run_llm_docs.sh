#!/bin/bash
# Quick script to generate LLM documentation from existing annotated.json

set -e

echo "=================================================="
echo "Generating LLM-Powered Documentation"
echo "=================================================="
echo ""

# Check if annotated.json exists
if [ ! -f "out/annotated.json" ]; then
    echo "Error: out/annotated.json not found!"
    echo "Run the basic annotation first:"
    echo "  ./process_video.sh design/softr.mp4"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found!"
    echo "Creating it now..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

echo ""

# Check API keys
MODELS=""
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ GEMINI_API_KEY detected"
    MODELS="gemini"
fi

if [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ OPENAI_API_KEY detected"
    if [ -n "$MODELS" ]; then
        MODELS="$MODELS openai"
    else
        MODELS="openai"
    fi
fi

if [ -z "$MODELS" ]; then
    echo ""
    echo "Error: No API keys found!"
    echo ""
    echo "Set at least one:"
    echo "  export GEMINI_API_KEY='your_key'"
    echo "  export OPENAI_API_KEY='your_key'"
    echo ""
    echo "Get keys from:"
    echo "  Gemini: https://aistudio.google.com/app/apikey"
    echo "  OpenAI: https://platform.openai.com/api-keys"
    exit 1
fi

echo ""
echo "Using models: $MODELS"
echo ""
echo "=================================================="
echo ""

# Run the LLM annotation
python3 llm_annotate.py out/annotated.json --models $MODELS

echo ""
echo "=================================================="
echo "✓ Documentation generated!"
echo "=================================================="
echo ""
echo "View results:"
echo "  open out/llm_docs/"
echo "  open out/llm_docs/README.md"
echo ""
echo "Documents created:"
for model in $MODELS; do
    echo "  - linear_walkthrough_${model}.md"
    echo "  - prd_document_${model}.md"
    echo "  - personas_stories_${model}.md"
done
echo ""
echo "=================================================="
