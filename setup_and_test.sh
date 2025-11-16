#!/bin/bash
# Setup and test the video annotation system

echo "=================================================="
echo "Video Annotation System - Setup & Test"
echo "=================================================="
echo ""

# Check system dependencies
echo "Checking system dependencies..."
echo ""

if command -v whisper &> /dev/null; then
    echo "✓ whisper installed ($(whisper --version 2>&1 | head -1))"
else
    echo "✗ whisper not installed"
    echo "  Install with: brew install openai-whisper"
    MISSING=1
fi

if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg installed ($(ffmpeg -version 2>&1 | head -1 | awk '{print $1, $3}'))"
else
    echo "✗ ffmpeg not installed"
    echo "  Install with: brew install ffmpeg"
    MISSING=1
fi

echo ""

# Check for virtual environment
echo "Checking virtual environment..."
echo ""

if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
    source venv/bin/activate
    VENV_ACTIVE=1
else
    echo "✗ Virtual environment not found"
    echo "  Will create during setup if needed"
fi

echo ""

# Check Python packages
echo "Checking Python packages..."
echo ""

if python3 -c "import google.generativeai" 2>/dev/null; then
    echo "✓ google-generativeai installed"
else
    echo "✗ google-generativeai not installed"
    echo "  Install with: pip install -r requirements.txt"
    MISSING_PY=1
fi

if python3 -c "import openai" 2>/dev/null; then
    echo "✓ openai installed"
else
    echo "✗ openai not installed"
    echo "  Install with: pip install -r requirements.txt"
    MISSING_PY=1
fi

echo ""

# Check API keys
echo "Checking API keys..."
echo ""

if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ GEMINI_API_KEY is set (${#GEMINI_API_KEY} chars)"
else
    echo "✗ GEMINI_API_KEY not set"
    echo "  Get key from: https://aistudio.google.com/app/apikey"
    echo "  Set with: export GEMINI_API_KEY='your_key'"
    MISSING_KEYS=1
fi

if [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ OPENAI_API_KEY is set (${#OPENAI_API_KEY} chars)"
else
    echo "✗ OPENAI_API_KEY not set"
    echo "  Get key from: https://platform.openai.com/api-keys"
    echo "  Set with: export OPENAI_API_KEY='your_key'"
    MISSING_KEYS=1
fi

echo ""
echo "=================================================="

if [ -n "$MISSING" ]; then
    echo ""
    echo "⚠ Missing system dependencies. Install them first:"
    echo "  brew install openai-whisper ffmpeg"
    echo ""
fi

if [ -n "$MISSING_PY" ]; then
    echo ""
    echo "⚠ Missing Python packages."
    echo ""
    echo "Install now? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Create venv if it doesn't exist
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        echo "Installing packages from requirements.txt..."
        pip install -r requirements.txt
        echo ""
        echo "✓ Python packages installed in virtual environment"
        echo "✓ To use later, run: source venv/bin/activate"
        echo ""
    fi
fi

if [ -n "$MISSING_KEYS" ]; then
    echo ""
    echo "⚠ API keys not set. You'll need these for LLM processing."
    echo "  Basic transcription and annotation will still work."
    echo ""
fi

# Test basic functionality
echo ""
echo "Testing basic scripts..."
echo ""

if [ -f "annotate_video.py" ] && [ -x "annotate_video.py" ]; then
    echo "✓ annotate_video.py is executable"
else
    echo "✗ annotate_video.py not found or not executable"
fi

if [ -f "llm_annotate.py" ] && [ -x "llm_annotate.py" ]; then
    echo "✓ llm_annotate.py is executable"
else
    echo "✗ llm_annotate.py not found or not executable"
fi

if [ -f "process_video.sh" ] && [ -x "process_video.sh" ]; then
    echo "✓ process_video.sh is executable"
else
    echo "✗ process_video.sh not found or not executable"
fi

echo ""

# Check if there's existing data to process
if [ -f "out/annotated.json" ]; then
    echo "=================================================="
    echo "Existing data found!"
    echo "=================================================="
    echo ""
    echo "You have an existing annotated transcript."
    echo "Run LLM processing on it? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if [ -z "$MISSING_KEYS" ]; then
            echo ""
            echo "Which models to use?"
            echo "1) Gemini only (faster, cheaper)"
            echo "2) OpenAI only"
            echo "3) Both (recommended for comparison)"
            read -r model_choice
            
            case $model_choice in
                1)
                    echo ""
                    echo "Running with Gemini..."
                    python3 llm_annotate.py out/annotated.json --models gemini
                    ;;
                2)
                    echo ""
                    echo "Running with OpenAI..."
                    python3 llm_annotate.py out/annotated.json --models openai
                    ;;
                3)
                    echo ""
                    echo "Running with both models..."
                    python3 llm_annotate.py out/annotated.json --models gemini openai
                    ;;
                *)
                    echo "Invalid choice"
                    ;;
            esac
        else
            echo "Cannot run LLM processing without API keys."
        fi
    fi
fi

echo ""
echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Process a video:"
echo "   ./process_video.sh design/your-video.mp4"
echo ""
echo "2. Or run steps manually (see QUICKSTART.md)"
echo ""
echo "3. View documentation:"
echo "   open LLM_ANNOTATION_README.md"
echo ""
echo "=================================================="
