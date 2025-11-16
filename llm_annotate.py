#!/usr/bin/env python3
"""
Generate comprehensive product documentation from annotated video transcripts.
Uses LLMs (Gemini and OpenAI) to create three types of documents:
1. Linear chapter/topic walkthrough
2. PRD/feature page-by-page document
3. Personas and user stories

Usage:
    python3 llm_annotate.py out/annotated.json --output-dir out/llm_docs --models gemini openai
"""
import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# LLM imports (install: pip install google-generativeai openai)
try:
    import google.generativeai as genai
except ImportError:
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai", file=sys.stderr)
    genai = None

try:
    from openai import OpenAI
except ImportError:
    print("Warning: openai not installed. Run: pip install openai", file=sys.stderr)
    OpenAI = None


class VideoAnnotationProcessor:
    """Process annotated video transcripts with LLMs to generate comprehensive documentation."""
    
    def __init__(self, annotated_json_path: str, output_dir: str):
        self.annotated_json_path = Path(annotated_json_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load annotated data
        with open(self.annotated_json_path) as f:
            self.data = json.load(f)
        
        self.items = self.data["items"]
        self.video_name = Path(self.data["video"]).stem
        
        # Setup API clients
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if self.gemini_key and genai:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.gemini_model = None
            
        if self.openai_key and OpenAI:
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None
    
    def prepare_transcript_context(self, max_items: Optional[int] = None) -> str:
        """Prepare the full transcript with timestamps for LLM context."""
        items = self.items[:max_items] if max_items else self.items
        
        lines = ["# Video Transcript with Timestamps\n"]
        for item in items:
            timestamp = item["start_hms"]
            text = item["text"]
            frame_info = f" [frame: {item['frame']['path']}]" if item.get("frame") else ""
            lines.append(f"**[{timestamp}]**{frame_info} {text}\n")
        
        return "\n".join(lines)
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API calls."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def prepare_frames_context(self, sample_rate: int = 5) -> List[Dict[str, Any]]:
        """Prepare sampled frames for visual context."""
        frames = []
        for i, item in enumerate(self.items):
            if i % sample_rate == 0 and item.get("frame"):
                frame_path = item["frame"]["path"]
                # Make path relative to annotated.json location
                if not Path(frame_path).is_absolute():
                    frame_path = self.annotated_json_path.parent / frame_path
                
                if Path(frame_path).exists():
                    frames.append({
                        "timestamp": item["start_hms"],
                        "path": str(frame_path),
                        "text": item["text"]
                    })
        return frames
    
    def call_gemini(self, prompt: str, frames: Optional[List[Dict]] = None) -> str:
        """Call Gemini API with text and optional images."""
        if not self.gemini_model:
            return "Error: Gemini API not configured"
        
        try:
            content = [prompt]
            
            if frames:
                for frame in frames:
                    if Path(frame["path"]).exists():
                        img = genai.upload_file(frame["path"])
                        content.append(img)
                        content.append(f"\n[Frame at {frame['timestamp']}]\n")
            
            response = self.gemini_model.generate_content(content)
            return response.text
        except Exception as e:
            return f"Error calling Gemini: {str(e)}"
    
    def call_openai(self, prompt: str, frames: Optional[List[Dict]] = None, model: str = "gpt-4o") -> str:
        """Call OpenAI API with text and optional images."""
        if not self.openai_client:
            return "Error: OpenAI API not configured"
        
        try:
            messages = [{"role": "user", "content": []}]
            
            # Add text prompt
            messages[0]["content"].append({
                "type": "text",
                "text": prompt
            })
            
            # Add images if provided
            if frames:
                for frame in frames:
                    if Path(frame["path"]).exists():
                        img_b64 = self.encode_image(frame["path"])
                        messages[0]["content"].append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}"
                            }
                        })
                        messages[0]["content"].append({
                            "type": "text",
                            "text": f"\n[Frame at {frame['timestamp']}]\n"
                        })
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=16000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
    
    def generate_linear_walkthrough(self, provider: str = "gemini") -> str:
        """Generate Document 1: Linear chapter/topic walkthrough with screenshots."""
        transcript = self.prepare_transcript_context()
        frames = self.prepare_frames_context(sample_rate=8)
        
        prompt = f"""You are analyzing a video walkthrough/demo of a software application.

{transcript}

Create a comprehensive LINEAR WALKTHROUGH document organized into chapters and topics. This should:

1. **Organize chronologically** by chapters/sections based on natural topic transitions
2. **For each chapter/topic, provide:**
   - Clear chapter title
   - Key takeaways (3-5 bullet points)
   - Detailed description of what the speaker is describing on-screen
   - Important UI elements, interactions, or workflows being demonstrated
   - Notable timestamps where key moments occur

3. **Writing style:**
   - Be faithful to what the speaker actually says and shows
   - Describe visual elements clearly (buttons, menus, layouts, colors, etc.)
   - Capture the flow and narrative of the demo
   - Note any tips, gotchas, or best practices mentioned

4. **Format as Markdown** with:
   - H2 (##) for chapters
   - H3 (###) for topics within chapters
   - Bullet points for key takeaways
   - Code blocks for any technical details
   - Referenced timestamps in [HH:MM:SS] format

Output a complete, well-structured Markdown document suitable for documentation.
"""
        
        print(f"Generating linear walkthrough with {provider}...")
        if provider == "gemini":
            result = self.call_gemini(prompt, frames)
        else:
            result = self.call_openai(prompt, frames)
        
        return result
    
    def generate_prd_document(self, provider: str = "gemini") -> str:
        """Generate Document 2: PRD/feature page-by-page document."""
        transcript = self.prepare_transcript_context()
        frames = self.prepare_frames_context(sample_rate=5)
        
        prompt = f"""You are creating a Product Requirements Document (PRD) from a video walkthrough of a software application.

{transcript}

Create a comprehensive PAGE-BY-PAGE PRD document suitable for rebuilding this application from scratch. This should:

1. **Identify all distinct pages/screens** shown in the video
2. **For each page, document:**
   - Page name and purpose
   - URL/navigation path (if mentioned)
   - Visual layout description
   - All UI components (buttons, forms, tables, menus, modals, etc.)
   - Features and functionality
   - Data displayed
   - User interactions available
   - Business logic and rules
   - Edge cases or validation mentioned

3. **Format as a proper PRD:**
   - Executive summary at top
   - Table of contents
   - Each page as a major section
   - Screenshots referenced by timestamp
   - Technical requirements
   - User interactions and workflows
   - Data models implied by the UI

4. **Be specific and detailed** - this should be comprehensive enough for developers to rebuild the exact UI and functionality.

Output a complete Markdown PRD document.
"""
        
        print(f"Generating PRD document with {provider}...")
        if provider == "gemini":
            result = self.call_gemini(prompt, frames)
        else:
            result = self.call_openai(prompt, frames)
        
        return result
    
    def generate_personas_and_stories(self, provider: str = "gemini") -> str:
        """Generate Document 3: Personas and user stories."""
        transcript = self.prepare_transcript_context()
        frames = self.prepare_frames_context(sample_rate=8)
        
        prompt = f"""You are creating user personas and user stories from a video walkthrough of a software application.

{transcript}

Create a comprehensive PERSONAS AND USER STORIES document that includes:

1. **User Personas (3-5 personas):**
   - Name and role
   - Background and context
   - Goals and motivations
   - Pain points and challenges
   - Technical skill level
   - How they would use this application

2. **User Stories for each page/feature:**
   - Format: "As a [persona], I want to [action] so that [benefit]"
   - Acceptance criteria
   - Priority (High/Medium/Low)
   - Related pages/features

3. **Feature Mapping:**
   - Map each major feature to relevant personas
   - Explain how each feature serves user needs
   - Note any workflows that span multiple pages

4. **User Journeys:**
   - End-to-end flows for common tasks
   - Entry points and exit points
   - Decision points and branches

5. **Screenshots and Context:**
   - Reference specific screens/timestamps
   - Explain what each screen accomplishes for users

Output a complete Markdown document with personas, user stories, and journeys.
"""
        
        print(f"Generating personas and user stories with {provider}...")
        if provider == "gemini":
            result = self.call_gemini(prompt, frames)
        else:
            result = self.call_openai(prompt, frames)
        
        return result
    
    def embed_screenshots_in_markdown(self, markdown_content: str) -> str:
        """Post-process markdown to embed screenshot image references at relevant timestamps."""
        # Remove markdown code fence if LLM wrapped output in it
        content = markdown_content.strip()
        if content.startswith('```markdown'):
            content = content[11:]  # Remove opening fence
        if content.startswith('```'):
            content = content[3:]   # Remove opening fence
        if content.endswith('```'):
            content = content[:-3]  # Remove closing fence
        content = content.strip()
        
        lines = content.split('\n')
        result = []
        
        # Pattern to find timestamp references like [00:00], **[01:23]**, etc.
        import re
        # Matches: [00:00], **[00:00]**, [00:00:00]
        timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Look for timestamp references in bullet points or headings
            matches = timestamp_pattern.findall(line)
            if matches and (line.strip().startswith('-') or line.strip().startswith('*') or '###' in line):
                # Get the first timestamp in the line
                ts = matches[0]
                
                # Find a frame close to this timestamp
                frame = self.find_frame_for_timestamp(ts)
                if frame:
                    # Don't add image if next line already has one
                    next_line = lines[i + 1] if i + 1 < len(lines) else ""
                    if not next_line.strip().startswith('!['):
                        # Make path relative to output markdown file (out/llm_docs/*.md -> out/frames/*.jpg = ../frames/*.jpg)
                        frame_path = Path(frame['path'])
                        # Get just the filename from the frame path
                        frame_filename = frame_path.name
                        rel_path = f"../frames/{frame_filename}"
                        result.append(f"\n![Screenshot at {ts}]({rel_path})\n")
        
        return '\n'.join(result)
    
    def find_frame_for_timestamp(self, timestamp_str: str) -> Optional[Dict]:
        """Find the frame closest to a given timestamp string (HH:MM or HH:MM:SS)."""
        # Parse timestamp to seconds
        parts = timestamp_str.split(':')
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            target_time = minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            target_time = hours * 3600 + minutes * 60 + seconds
        else:
            return None
        
        # Find closest frame
        best_frame = None
        min_diff = float('inf')
        
        for item in self.items:
            if item.get('frame'):
                frame_time = item['start']
                diff = abs(frame_time - target_time)
                if diff < min_diff:
                    min_diff = diff
                    frame_path = item['frame']['path']
                    
                    # Handle path resolution
                    if not Path(frame_path).is_absolute():
                        # If path already starts with 'out/', use from project root
                        if frame_path.startswith('out/'):
                            # Get project root (parent of annotated.json's parent)
                            project_root = self.annotated_json_path.parent.parent
                            frame_path = project_root / frame_path
                        else:
                            # Otherwise relative to annotated.json
                            frame_path = self.annotated_json_path.parent / frame_path
                    
                    if Path(frame_path).exists():
                        best_frame = {
                            'path': str(frame_path),
                            'timestamp': item['start_hms']
                        }
        
        # Only return if within 30 seconds
        if min_diff <= 30:
            return best_frame
        return None
    
    def generate_all_documents(self, providers: List[str] = ["gemini"]):
        """Generate all three documents with specified LLM providers."""
        documents = {
            "linear_walkthrough": self.generate_linear_walkthrough,
            "prd_document": self.generate_prd_document,
            "personas_stories": self.generate_personas_and_stories
        }
        
        for doc_type, generator_func in documents.items():
            for provider in providers:
                print(f"\n{'='*60}")
                print(f"Generating {doc_type} with {provider}...")
                print(f"{'='*60}\n")
                
                result = generator_func(provider=provider)
                
                # Embed screenshots at timestamp references
                print(f"Embedding screenshots...")
                result_with_screenshots = self.embed_screenshots_in_markdown(result)
                screenshots_added = result_with_screenshots.count('![Screenshot')
                if screenshots_added > 0:
                    print(f"  ✓ Added {screenshots_added} screenshots")
                
                # Save output
                output_file = self.output_dir / f"{doc_type}_{provider}.md"
                output_file.write_text(result_with_screenshots)
                print(f"✓ Saved to {output_file}\n")
        
        # Generate comparison summary
        if len(providers) > 1:
            self.generate_comparison_summary(providers)
    
    def generate_comparison_summary(self, providers: List[str]):
        """Generate a summary comparing outputs from different providers."""
        summary = [f"# LLM Comparison Summary - {self.video_name}\n"]
        summary.append(f"Generated {len(providers)} versions of each document type.\n")
        summary.append("## Providers\n")
        for p in providers:
            summary.append(f"- {p}")
        summary.append("\n## Documents Generated\n")
        summary.append("1. **Linear Walkthrough** - Chapter/topic organized with timestamps")
        summary.append("2. **PRD Document** - Page-by-page feature specifications")
        summary.append("3. **Personas & User Stories** - User-centric documentation\n")
        summary.append("## Files\n")
        
        for doc_type in ["linear_walkthrough", "prd_document", "personas_stories"]:
            summary.append(f"\n### {doc_type.replace('_', ' ').title()}\n")
            for provider in providers:
                filename = f"{doc_type}_{provider}.md"
                summary.append(f"- `{filename}`")
        
        summary_file = self.output_dir / "README.md"
        summary_file.write_text("\n".join(summary))
        print(f"✓ Comparison summary saved to {summary_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive documentation from annotated video transcripts using LLMs"
    )
    parser.add_argument(
        "annotated_json",
        help="Path to annotated.json file from annotate_video.py"
    )
    parser.add_argument(
        "--output-dir",
        default="out/llm_docs",
        help="Output directory for generated documents (default: out/llm_docs)"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=["gemini", "openai"],
        default=["gemini"],
        help="LLM providers to use (can specify multiple for comparison)"
    )
    
    args = parser.parse_args()
    
    # Check for API keys
    if "gemini" in args.models and not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    if "openai" in args.models and not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Process
    processor = VideoAnnotationProcessor(args.annotated_json, args.output_dir)
    processor.generate_all_documents(providers=args.models)
    
    print("\n" + "="*60)
    print("✓ All documents generated successfully!")
    print(f"✓ Output directory: {args.output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
