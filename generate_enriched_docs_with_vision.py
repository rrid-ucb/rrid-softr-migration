#!/usr/bin/env python3
"""
Generate enriched documentation using Gemini Vision to analyze all 168 screenshots.

This script:
1. Loads all frames with timestamps and transcript segments
2. Uses Gemini Vision to analyze each screenshot
3. Generates enriched linear walkthrough that goes beyond speaker narration
4. Generates enriched PRD and personas documents
5. Saves to out/llm_docs_enriched/ directory
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed. Run: pip install google-generativeai", file=sys.stderr)
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("Warning: tqdm not installed. Install with: pip install tqdm", file=sys.stderr)
    # Fallback: create a dummy tqdm that does nothing
    def tqdm(iterable=None, **kwargs):
        if iterable is None:
            class DummyTqdm:
                def __init__(self, **kwargs):
                    pass
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def update(self, n=1):
                    pass
                def set_description(self, desc):
                    print(f"  {desc}")
                def close(self):
                    pass
            return DummyTqdm(**kwargs)
        return iterable


class EnrichedDocGenerator:
    """Generate enriched documentation using Gemini Vision."""
    
    def __init__(self, annotated_json_path: Path, frames_timestamps_path: Path, frames_dir: Path, output_dir: Path):
        self.annotated_json_path = annotated_json_path
        self.frames_timestamps_path = frames_timestamps_path
        self.frames_dir = frames_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data
        with open(annotated_json_path) as f:
            self.annotated_data = json.load(f)
        
        with open(frames_timestamps_path) as f:
            self.frames_data = json.load(f)
        
        # Setup Gemini
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_key:
            print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
            sys.exit(1)
        
        genai.configure(api_key=self.gemini_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Create mapping: timestamp -> (frame_filename, transcript_item)
        self.timestamp_to_frame = {}
        self.timestamp_to_item = {}
        
        for frame_info in self.frames_data:
            timestamp = frame_info['timestamp']
            filename = frame_info['filename']
            self.timestamp_to_frame[timestamp] = filename
        
        for item in self.annotated_data.get("items", []):
            timestamp = item.get("start_hms", "")
            if timestamp:
                self.timestamp_to_item[timestamp] = item
    
    def get_frame_path(self, filename: str) -> Path:
        """Get full path to frame file."""
        return self.frames_dir / filename
    
    def call_gemini_vision(self, prompt: str, image_paths: List[Path], frame_info_list: Optional[List[Dict]] = None, verbose: bool = True) -> str:
        """Call Gemini Vision API with text prompt and images."""
        try:
            if verbose:
                print(f"    Preparing {len(image_paths)} images for Gemini Vision API...")
            
            content = [prompt]
            
            upload_start = time.time()
            for i, img_path in enumerate(image_paths):
                if img_path.exists():
                    if verbose and i % 5 == 0:
                        print(f"    Uploading image {i+1}/{len(image_paths)}: {img_path.name}")
                    
                    # Upload file to Gemini
                    uploaded_file = genai.upload_file(str(img_path))
                    content.append(uploaded_file)
                    
                    # Add context about this frame if available
                    if frame_info_list and i < len(frame_info_list):
                        frame_info = frame_info_list[i]
                        timestamp = frame_info.get('timestamp', '')
                        filename = frame_info.get('filename', img_path.name)
                        content.append(f"\n[Frame: {filename} at timestamp {timestamp}]\n")
            
            upload_time = time.time() - upload_start
            if verbose:
                print(f"    ✓ Uploaded {len(image_paths)} images in {upload_time:.1f}s")
                print(f"    Sending request to Gemini Vision API...")
            
            api_start = time.time()
            response = self.model.generate_content(content)
            api_time = time.time() - api_start
            
            if verbose:
                print(f"    ✓ Received response in {api_time:.1f}s")
                print(f"    Response length: {len(response.text)} characters")
            
            return response.text
        except Exception as e:
            error_msg = f"Error calling Gemini Vision: {str(e)}"
            if verbose:
                print(f"    ✗ {error_msg}")
            return error_msg
    
    def process_frames_in_batches(self, chapter_duration_minutes: float = 2.5) -> List[Dict]:
        """Process frames in batches, breaking into chapters by time intervals."""
        # Group frames into chapters based on time intervals (every ~2.5 minutes)
        frames_by_chapter = []
        current_chapter = []
        chapter_start_seconds = 0
        chapter_duration_seconds = chapter_duration_minutes * 60
        
        for frame_info in self.frames_data:
            seconds = frame_info['timestamp_seconds']
            
            # Start new chapter if we've exceeded the chapter duration
            if seconds >= chapter_start_seconds + chapter_duration_seconds:
                if current_chapter:
                    frames_by_chapter.append(current_chapter)
                current_chapter = []
                chapter_start_seconds = seconds
            
            current_chapter.append(frame_info)
        
        if current_chapter:
            frames_by_chapter.append(current_chapter)
        
        return frames_by_chapter
    
    def generate_enriched_linear_walkthrough(self) -> str:
        """Generate enriched linear walkthrough using vision analysis."""
        print("\n" + "=" * 60)
        print("Generating Enriched Linear Walkthrough with Gemini Vision")
        print("=" * 60)
        
        # Process frames in chapters (break into ~2.5 minute intervals)
        chapters = self.process_frames_in_batches(chapter_duration_minutes=2.5)
        total_chapters = len(chapters)
        print(f"Processing {total_chapters} chapters with {len(self.frames_data)} total frames\n")
        
        enriched_content = []
        enriched_content.append("# Enriched Linear Walkthrough - Comprehensive Analysis\n")
        enriched_content.append("This document provides a comprehensive walkthrough enriched with visual analysis of all screenshots.\n")
        enriched_content.append("It goes beyond the speaker's narration to identify Softr interface components, Airtable integrations, and UI details.\n\n")
        
        chapter_num = 1
        
        # Use tqdm for progress bar
        with tqdm(total=total_chapters, desc="Processing chapters", unit="chapter") as pbar:
            for chapter_frames in chapters:
                if not chapter_frames:
                    continue
                
                # Get time range for this chapter
                first_frame = chapter_frames[0]
                last_frame = chapter_frames[-1]
                start_time = first_frame['timestamp']
                end_time = last_frame['timestamp']
                
                pbar.set_description(f"Chapter {chapter_num}/{total_chapters} ({start_time}-{end_time})")
                print(f"\n[Chapter {chapter_num}/{total_chapters}] Processing: {start_time} - {end_time}")
                print(f"  Frames in chapter: {len(chapter_frames)}")
                
                # Prepare transcript for this chapter (more comprehensive)
                chapter_transcript = []
                for frame_info in chapter_frames:
                    timestamp = frame_info['timestamp']
                    if timestamp in self.timestamp_to_item:
                        item = self.timestamp_to_item[timestamp]
                        chapter_transcript.append(f"**[{timestamp}]** {item.get('text', '')}")
                
                # Prepare images for this chapter
                image_paths = []
                frame_info_list = []
                for frame_info in chapter_frames:
                    filename = frame_info['filename']
                    img_path = self.get_frame_path(filename)
                    if img_path.exists():
                        image_paths.append(img_path)
                        frame_info_list.append(frame_info)
                
                if not image_paths:
                    chapter_num += 1
                    pbar.update(1)
                    continue
                
                # Limit images per API call (Gemini has limits) but try to get more frames per chapter
                max_images_per_call = 16
                if len(image_paths) > max_images_per_call:
                    # Sample frames evenly to get representative coverage
                    step = max(1, len(image_paths) // max_images_per_call)
                    image_paths = image_paths[::step][:max_images_per_call]
                    frame_info_list = frame_info_list[::step][:max_images_per_call]
                
                # Create comprehensive prompt for this chapter
                transcript_sample = "\n".join(chapter_transcript[:20])  # More transcript context
                
                prompt = f"""You are analyzing screenshots from a Softr application walkthrough video to create a comprehensive chapter for a linear walkthrough document.

**IMPORTANT**: Be extremely verbose and detailed. This is Chapter {chapter_num} of {total_chapters}. Create a complete, standalone chapter that matches the quality and depth of the other chapters in the document.

The speaker's transcript for this chapter ({start_time} - {end_time}) is:
{transcript_sample}

Please analyze the {len(image_paths)} screenshots provided and create a comprehensive chapter that includes:

## Chapter {chapter_num}: [Descriptive Title Based on Content]

### Key Takeaways
- 3-5 bullet points summarizing what the speaker explains AND what you observe in the UI
- Focus on both narration and visual details

### Detailed Description
Provide a rich, detailed description that goes beyond the narration to describe:
- Softr interface components visible (buttons, forms, lists, filters, tables, etc.)
- Airtable integration points (data sources, field types, relationships visible in the UI)
- UI/UX patterns and design elements
- Navigation elements and structure
- Data relationships and workflows visible in the interface
- Technical details you can infer from the screenshots
- Any Softr-specific features or configurations visible

### Important UI Elements and Interactions
- Detailed breakdown of all visible UI elements
- How users interact with the interface
- Role-based differences if visible
- Form fields, buttons, filters, and their purposes

### Notable Timestamps
- Key moments with screenshot references using format: ![Screenshot at TIMESTAMP](../frames/frame_XXXXX_TIMESTAMP.jpg)
- Include multiple timestamps throughout the chapter
- Reference specific frames that illustrate important points

**Format Requirements:**
- Use proper markdown formatting (## for chapter title, ### for subsections)
- Include horizontal rule (---) at the end of the chapter
- Reference screenshots using the exact format: ![Screenshot at TIMESTAMP](../frames/frame_XXXXX_TIMESTAMP.jpg)
- Be as detailed and comprehensive as possible - this should be a rich, informative chapter"""
                
                # Call Gemini Vision
                try:
                    print(f"  Calling Gemini Vision API for Chapter {chapter_num}...")
                    vision_response = self.call_gemini_vision(prompt, image_paths, frame_info_list, verbose=True)
                    
                    if vision_response.startswith("Error"):
                        print(f"  ✗ {vision_response}")
                        enriched_content.append(f"\n## Chapter {chapter_num}: {start_time} - {end_time}\n\n")
                        enriched_content.append(f"*[Error processing this chapter: {vision_response}]*\n")
                    else:
                        # Add the chapter content (Gemini should include the chapter header)
                        enriched_content.append(vision_response)
                        enriched_content.append("\n")
                        print(f"  ✓ Successfully generated content for Chapter {chapter_num}")
                    
                except Exception as e:
                    print(f"  ✗ Exception processing chapter {chapter_num}: {e}")
                    import traceback
                    print(f"  Traceback: {traceback.format_exc()}")
                    # Fallback: add basic chapter
                    enriched_content.append(f"\n## Chapter {chapter_num}: {start_time} - {end_time}\n\n")
                    enriched_content.append(f"*[Error processing this chapter: {str(e)}]*\n")
                
                chapter_num += 1
                pbar.update(1)
        
        return "\n".join(enriched_content)
    
    def generate_enriched_prd(self) -> str:
        """Generate enriched PRD document using vision analysis."""
        print("\n" + "=" * 60)
        print("Generating Enriched PRD Document with Gemini Vision")
        print("=" * 60)
        
        # Sample key frames for PRD (focus on different pages/features)
        key_frames = []
        seen_pages = set()
        
        # Get frames that represent different pages/features
        for frame_info in self.frames_data[::10]:  # Sample every 10th frame
            timestamp = frame_info['timestamp']
            if timestamp in self.timestamp_to_item:
                item = self.timestamp_to_item[timestamp]
                text = item.get('text', '').lower()
                
                # Identify different pages/features
                if any(keyword in text for keyword in ['landing', 'page', 'home']):
                    if 'landing' not in seen_pages:
                        key_frames.append(frame_info)
                        seen_pages.add('landing')
                elif any(keyword in text for keyword in ['preprint', 'list']):
                    if 'preprint' not in seen_pages:
                        key_frames.append(frame_info)
                        seen_pages.add('preprint')
                elif any(keyword in text for keyword in ['reviewer', 'propose']):
                    if 'reviewer' not in seen_pages:
                        key_frames.append(frame_info)
                        seen_pages.add('reviewer')
                elif any(keyword in text for keyword in ['quality', 'check']):
                    if 'quality' not in seen_pages:
                        key_frames.append(frame_info)
                        seen_pages.add('quality')
                elif any(keyword in text for keyword in ['dashboard', 'productivity']):
                    if 'dashboard' not in seen_pages:
                        key_frames.append(frame_info)
                        seen_pages.add('dashboard')
        
        # Add more frames if we don't have enough
        if len(key_frames) < 20:
            key_frames.extend(self.frames_data[::8][:20])
        
        # Prepare images
        image_paths = []
        frame_info_list = []
        for frame_info in key_frames[:30]:  # Limit to 30 frames for PRD
            filename = frame_info['filename']
            timestamp = frame_info['timestamp']
            img_path = self.get_frame_path(filename)
            if img_path.exists():
                image_paths.append(img_path)
                frame_info_list.append(frame_info)
        
        # Limit to 16 images per call
        if len(image_paths) > 16:
            step = len(image_paths) // 16
            image_paths = image_paths[::max(step, 1)][:16]
            frame_info_list = frame_info_list[::max(step, 1)][:16]
        
        prompt = f"""You are analyzing screenshots from a Softr application to create a comprehensive Product Requirements Document (PRD).

**IMPORTANT**: Be extremely detailed and verbose. Describe every UI element, component, and technical detail you can see in the screenshots.

The application appears to be a peer review management system built on Softr (which integrates with Airtable).

From the {len(image_paths)} screenshots provided, create a detailed PRD that includes:

1. **Executive Summary** - Overview of the application
2. **Page-by-Page Specifications** - For each distinct page/feature visible:
   - Purpose and URL/Navigation Path
   - Visual Layout (detailed description)
   - UI Components (buttons, forms, tables, filters, etc.)
   - Features and Functionality
   - Data Displayed (what data is shown and how)
   - User Interactions (what users can do)
   - Business Logic (inferred from UI)
   - Edge Cases/Validation
   - Airtable Integration Points (if visible)
   - Softr-Specific Components (forms, lists, views, etc.)
3. **Technical Requirements** - Based on what you see
4. **Data Models** - Inferred from the UI
5. **User Workflows** - Based on navigation and interactions visible

Focus on what's actually visible in the screenshots. Identify Softr components, Airtable field types, relationship structures, and any technical details you can infer.

Format as comprehensive markdown. For each screenshot, reference it using: ![Screenshot at TIMESTAMP](../frames/frame_XXXXX_TIMESTAMP.jpg) where TIMESTAMP matches the frame filename."""
        
        print(f"Analyzing {len(image_paths)} key frames for PRD...")
        try:
            prd_content = self.call_gemini_vision(prompt, image_paths, frame_info_list, verbose=True)
            if prd_content.startswith("Error"):
                print(f"✗ Error: {prd_content}")
            else:
                print(f"✓ Successfully generated PRD ({len(prd_content)} characters)")
            return f"# Enriched Product Requirements Document (PRD)\n\n{prd_content}"
        except Exception as e:
            print(f"✗ Exception generating PRD: {e}")
            import traceback
            print(traceback.format_exc())
            return f"# Enriched Product Requirements Document (PRD)\n\n*Error generating PRD: {str(e)}*"
    
    def generate_enriched_personas(self) -> str:
        """Generate enriched personas and user stories using vision analysis."""
        print("\n" + "=" * 60)
        print("Generating Enriched Personas Document with Gemini Vision")
        print("=" * 60)
        
        # Sample frames that show different user perspectives/workflows
        key_frames = []
        for frame_info in self.frames_data[::15]:  # Sample every 15th frame
            timestamp = frame_info['timestamp']
            if timestamp in self.timestamp_to_item:
                item = self.timestamp_to_item[timestamp]
                text = item.get('text', '').lower()
                
                # Collect frames that show different user roles/workflows
                if any(keyword in text for keyword in ['student', 'view', 'propose']):
                    key_frames.append(frame_info)
                elif any(keyword in text for keyword in ['editor', 'quality', 'check']):
                    key_frames.append(frame_info)
                elif any(keyword in text for keyword in ['dashboard', 'productivity', 'team']):
                    key_frames.append(frame_info)
        
        # Limit to 25 frames
        key_frames = key_frames[:25]
        
        # Prepare images
        image_paths = []
        frame_info_list = []
        for frame_info in key_frames:
            filename = frame_info['filename']
            img_path = self.get_frame_path(filename)
            if img_path.exists():
                image_paths.append(img_path)
                frame_info_list.append(frame_info)
        
        # Limit to 16 images per call
        if len(image_paths) > 16:
            step = len(image_paths) // 16
            image_paths = image_paths[::max(step, 1)][:16]
            frame_info_list = frame_info_list[::max(step, 1)][:16]
        
        prompt = f"""You are analyzing screenshots from a Softr peer review management application to create comprehensive user personas and stories.

**IMPORTANT**: Be detailed and verbose. Analyze every visible UI element, role-based difference, and workflow pattern you can identify.

From the {len(image_paths)} screenshots provided, create:

1. **User Personas** - Identify distinct user roles visible:
   - Role and background
   - Goals and motivations (inferred from UI access)
   - Pain points and challenges
   - Technical skill level
   - How they use the application (based on what's visible)

2. **User Stories** - Based on workflows visible in the UI:
   - As a [persona], I want to [action] so that [benefit]
   - Acceptance criteria
   - Priority
   - Related pages/features

3. **Feature Mapping** - Map features to personas based on UI visibility

4. **User Journeys** - Detailed workflows based on navigation and interactions visible:
   - Entry points
   - Task flows
   - Exit points
   - Decision points

5. **Screenshots and Context** - Reference specific screenshots that illustrate each persona/story

Focus on what's actually visible in the UI - different views, permissions, workflows, etc. Identify role-based differences you can see in the screenshots.

Format as comprehensive markdown. For each screenshot, reference it using: ![Screenshot at TIMESTAMP](../frames/frame_XXXXX_TIMESTAMP.jpg) where TIMESTAMP matches the frame filename."""
        
        print(f"Analyzing {len(image_paths)} key frames for personas...")
        try:
            personas_content = self.call_gemini_vision(prompt, image_paths, frame_info_list, verbose=True)
            if personas_content.startswith("Error"):
                print(f"✗ Error: {personas_content}")
            else:
                print(f"✓ Successfully generated personas document ({len(personas_content)} characters)")
            return f"# Enriched Personas, User Stories, and User Journeys\n\n{personas_content}"
        except Exception as e:
            print(f"✗ Exception generating personas: {e}")
            import traceback
            print(traceback.format_exc())
            return f"# Enriched Personas, User Stories, and User Journeys\n\n*Error generating personas: {str(e)}*"
    
    def generate_all(self):
        """Generate all enriched documents."""
        start_time = time.time()
        
        print("=" * 60)
        print("Generating Enriched Documentation with Gemini Vision")
        print("=" * 60)
        print(f"Total frames to analyze: {len(self.frames_data)}")
        print(f"Output directory: {self.output_dir}")
        print(f"API Key: {'✓ Set' if self.gemini_key else '✗ Not Set'}")
        print("=" * 60)
        
        try:
            # Generate linear walkthrough
            print("\n[1/3] Generating Linear Walkthrough...")
            linear_content = self.generate_enriched_linear_walkthrough()
            linear_path = self.output_dir / "linear_walkthrough_enriched.md"
            linear_path.write_text(linear_content)
            linear_size = linear_path.stat().st_size / 1024  # KB
            print(f"\n✓ Saved: {linear_path} ({linear_size:.1f} KB)")
            
            # Generate PRD
            print("\n[2/3] Generating PRD Document...")
            prd_content = self.generate_enriched_prd()
            prd_path = self.output_dir / "prd_document_enriched.md"
            prd_path.write_text(prd_content)
            prd_size = prd_path.stat().st_size / 1024  # KB
            print(f"\n✓ Saved: {prd_path} ({prd_size:.1f} KB)")
            
            # Generate personas
            print("\n[3/3] Generating Personas Document...")
            personas_content = self.generate_enriched_personas()
            personas_path = self.output_dir / "personas_stories_enriched.md"
            personas_path.write_text(personas_content)
            personas_size = personas_path.stat().st_size / 1024  # KB
            print(f"\n✓ Saved: {personas_path} ({personas_size:.1f} KB)")
            
            total_time = time.time() - start_time
            print("\n" + "=" * 60)
            print("✓ Complete! All enriched documents generated.")
            print(f"Total time: {total_time/60:.1f} minutes")
            print(f"Output directory: {self.output_dir}")
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user. Partial results may be saved.")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n✗ Fatal error: {e}")
            import traceback
            print(traceback.format_exc())
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate enriched documentation using Gemini Vision"
    )
    parser.add_argument(
        "--annotated-json",
        default="out/annotated.json",
        help="Path to annotated.json file"
    )
    parser.add_argument(
        "--frames-timestamps",
        default="out/frames/frames_timestamps.json",
        help="Path to frames_timestamps.json"
    )
    parser.add_argument(
        "--frames-dir",
        default="out/frames",
        help="Directory containing frames"
    )
    parser.add_argument(
        "--output-dir",
        default="out/llm_docs_enriched",
        help="Output directory for enriched documents"
    )
    
    args = parser.parse_args()
    
    annotated_json_path = Path(args.annotated_json)
    frames_timestamps_path = Path(args.frames_timestamps)
    frames_dir = Path(args.frames_dir)
    output_dir = Path(args.output_dir)
    
    # Validate inputs
    if not annotated_json_path.exists():
        print(f"Error: Annotated JSON not found: {annotated_json_path}", file=sys.stderr)
        sys.exit(1)
    
    if not frames_timestamps_path.exists():
        print(f"Error: Frames timestamps file not found: {frames_timestamps_path}", file=sys.stderr)
        sys.exit(1)
    
    if not frames_dir.exists():
        print(f"Error: Frames directory not found: {frames_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export GEMINI_API_KEY='your_key'", file=sys.stderr)
        sys.exit(1)
    
    # Generate enriched docs
    generator = EnrichedDocGenerator(
        annotated_json_path,
        frames_timestamps_path,
        frames_dir,
        output_dir
    )
    
    generator.generate_all()


if __name__ == "__main__":
    main()

