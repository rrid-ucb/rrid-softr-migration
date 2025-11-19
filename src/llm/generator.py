"""
LLM-powered document generation with model management.
"""

import base64
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from ..config.manager import ConfigManager


class LLMDocumentGenerator:
    """Generate documentation using LLMs with configured models."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
        # Setup API clients
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.gemini_model = None
        self.openai_client = None
        
        if self.gemini_key and genai:
            genai.configure(api_key=self.gemini_key)
            vision_model = self.config.get_model('vision')
            model_name = 'gemini-2.0-flash-exp'  # Default
            if vision_model and vision_model.get('provider') == 'gemini':
                model_name = vision_model.get('name', model_name)
            try:
                self.gemini_model = genai.GenerativeModel(model_name)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini model: {e}", file=sys.stderr)
        
        if self.openai_key and OpenAI:
            try:
                self.openai_client = OpenAI(api_key=self.openai_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}", file=sys.stderr)
    
    def generate_documents(
        self,
        annotated_json_path: Path,
        frames_dir: Path,
        output_dir: Path,
        providers: Optional[List[str]] = None
    ):
        """
        Generate all document types using configured models.
        
        Args:
            annotated_json_path: Path to annotated.json
            frames_dir: Directory containing frames
            output_dir: Output directory for generated documents
            providers: Optional list of providers to use (defaults to configured)
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load annotated data
        with open(annotated_json_path) as f:
            data = json.load(f)
        
        # Determine which providers to use
        if providers is None:
            providers = []
            if self.gemini_model:
                providers.append('gemini')
            if self.openai_client:
                providers.append('openai')
        
        if not providers:
            print("Warning: No LLM providers available. Set GEMINI_API_KEY or OPENAI_API_KEY.")
            return
        
        print(f"\nGenerating documents with providers: {', '.join(providers)}")
        
        # Generate each document type
        for provider in providers:
            suffix = f"_{provider}" if len(providers) > 1 else ""
            
            # Linear walkthrough
            print(f"\n[{provider}] Generating linear walkthrough...")
            linear_content = self._generate_linear_walkthrough(data, frames_dir, provider)
            if linear_content:
                linear_content = self._embed_screenshots(linear_content, data, frames_dir, annotated_json_path)
                (output_dir / f"linear_walkthrough{suffix}.md").write_text(linear_content)
            
            # PRD document
            print(f"[{provider}] Generating PRD...")
            prd_content = self._generate_prd(data, frames_dir, provider)
            if prd_content:
                prd_content = self._embed_screenshots(prd_content, data, frames_dir, annotated_json_path)
                (output_dir / f"prd_document{suffix}.md").write_text(prd_content)
            
            # Personas
            print(f"[{provider}] Generating personas...")
            personas_content = self._generate_personas(data, frames_dir, provider)
            if personas_content:
                personas_content = self._embed_screenshots(personas_content, data, frames_dir, annotated_json_path)
                (output_dir / f"personas_stories{suffix}.md").write_text(personas_content)
            
            # Issues document (for Airtable/backend videos)
            print(f"[{provider}] Generating issues document...")
            issues_content = self._generate_issues(data, frames_dir, provider)
            if issues_content:
                issues_content = self._embed_screenshots(issues_content, data, frames_dir, annotated_json_path)
                (output_dir / f"issues{suffix}.md").write_text(issues_content)
        
        print(f"\n✓ Documents generated in: {output_dir}")
    
    def _prepare_transcript_context(self, data: dict, max_items: Optional[int] = None) -> str:
        """Prepare the full transcript with timestamps for LLM context."""
        items = data.get('items', [])
        items = items[:max_items] if max_items else items
        
        lines = ["# Video Transcript with Timestamps\n"]
        for item in items:
            timestamp = item.get("start_hms", "")
            text = item.get("text", "")
            frame_info = f" [frame: {item['frame']['path']}]" if item.get("frame") else ""
            lines.append(f"**[{timestamp}]**{frame_info} {text}\n")
        
        return "\n".join(lines)
    
    def _prepare_frames_context(self, data: dict, frames_dir: Path, sample_rate: int = 5) -> List[Dict[str, Any]]:
        """Prepare sampled frames for visual context."""
        items = data.get('items', [])
        frames = []
        for i, item in enumerate(items):
            if i % sample_rate == 0 and item.get("frame"):
                frame_path = item["frame"]["path"]
                # Resolve path relative to frames_dir
                if not Path(frame_path).is_absolute():
                    frame_path = frames_dir / Path(frame_path).name
                
                if Path(frame_path).exists():
                    frames.append({
                        "timestamp": item.get("start_hms", ""),
                        "path": str(frame_path),
                        "text": item.get("text", "")
                    })
        return frames
    
    def _call_gemini(self, prompt: str, frames: Optional[List[Dict]] = None) -> str:
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
    
    def _call_openai(self, prompt: str, frames: Optional[List[Dict]] = None, model: str = "gpt-4o") -> str:
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
                        img_b64 = base64.b64encode(Path(frame["path"]).read_bytes()).decode('utf-8')
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
    
    def _generate_linear_walkthrough(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate linear walkthrough document."""
        transcript = self._prepare_transcript_context(data)
        frames = self._prepare_frames_context(data, frames_dir, sample_rate=8)
        
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
        
        if provider == "gemini":
            return self._call_gemini(prompt, frames)
        else:
            return self._call_openai(prompt, frames)
    
    def _generate_prd(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate PRD document."""
        transcript = self._prepare_transcript_context(data)
        frames = self._prepare_frames_context(data, frames_dir, sample_rate=5)
        
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
        
        if provider == "gemini":
            return self._call_gemini(prompt, frames)
        else:
            return self._call_openai(prompt, frames)
    
    def _generate_personas(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate personas document."""
        transcript = self._prepare_transcript_context(data)
        frames = self._prepare_frames_context(data, frames_dir, sample_rate=8)
        
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
        
        if provider == "gemini":
            return self._call_gemini(prompt, frames)
        else:
            return self._call_openai(prompt, frames)
    
    def _generate_issues(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate issues and pain points document."""
        transcript = self._prepare_transcript_context(data)
        frames = self._prepare_frames_context(data, frames_dir, sample_rate=5)
        
        prompt = f"""You are analyzing a video walkthrough that discusses backend systems, automations, integrations, or technical architecture.

{transcript}

Create a comprehensive ISSUES AND PAIN POINTS document that catalogs:

1. **Problems Identified:**
   - Technical issues mentioned by the speaker
   - Bugs or errors encountered
   - Performance problems
   - Data inconsistencies
   - Integration failures
   - Automation problems

2. **Pain Points:**
   - Workflow inefficiencies
   - User experience frustrations
   - Manual workarounds required
   - Confusing or unclear processes
   - Missing features or capabilities
   - Scalability concerns

3. **Architecture Concerns:**
   - System limitations
   - Technical debt mentioned
   - Maintenance challenges
   - Dependency issues
   - Data flow problems
   - Security concerns

4. **For each issue/pain point, document:**
   - Description of the problem
   - When/where it occurs (timestamp references)
   - Impact on users or system
   - Workarounds mentioned (if any)
   - Suggested solutions (if mentioned)
   - Priority/severity (if indicated)

5. **Categorize issues by:**
   - System/component affected
   - Type (bug, feature gap, performance, UX, etc.)
   - User impact level

Format as a well-organized Markdown document with clear sections and timestamps for reference.
"""
        
        if provider == "gemini":
            return self._call_gemini(prompt, frames)
        else:
            return self._call_openai(prompt, frames)
    
    def _find_frame_for_timestamp(self, timestamp_str: str, data: dict, frames_dir: Path) -> Optional[Dict]:
        """Find the frame closest to a given timestamp string."""
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
        
        items = data.get('items', [])
        for item in items:
            if item.get('frame'):
                frame_time = item.get('start', 0)
                diff = abs(frame_time - target_time)
                if diff < min_diff:
                    min_diff = diff
                    frame_path = item['frame']['path']
                    
                    # Resolve path
                    if not Path(frame_path).is_absolute():
                        frame_path = frames_dir / Path(frame_path).name
                    
                    if Path(frame_path).exists():
                        best_frame = {
                            'path': str(frame_path),
                            'timestamp': item.get('start_hms', '')
                        }
        
        # Only return if within 30 seconds
        if min_diff <= 30:
            return best_frame
        return None
    
    def _embed_screenshots(self, markdown_content: str, data: dict, frames_dir: Path, annotated_json_path: Path) -> str:
        """Post-process markdown to embed screenshot image references at relevant timestamps."""
        # Remove markdown code fence if LLM wrapped output in it
        content = markdown_content.strip()
        if content.startswith('```markdown'):
            content = content[11:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        lines = content.split('\n')
        result = []
        
        # Pattern to find timestamp references like [00:00], **[01:23]**, etc.
        timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Look for timestamp references in bullet points or headings
            matches = timestamp_pattern.findall(line)
            if matches and (line.strip().startswith('-') or line.strip().startswith('*') or '###' in line):
                # Get the first timestamp in the line
                ts = matches[0]
                
                # Find a frame close to this timestamp
                frame = self._find_frame_for_timestamp(ts, data, frames_dir)
                if frame:
                    # Don't add image if next line already has one
                    next_line = lines[i + 1] if i + 1 < len(lines) else ""
                    if not next_line.strip().startswith('!['):
                        # Make path relative to output markdown file
                        frame_filename = Path(frame['path']).name
                        rel_path = f"../frames/{frame_filename}"
                        result.append(f"\n![Screenshot at {ts}]({rel_path})\n")
        
        return '\n'.join(result)

