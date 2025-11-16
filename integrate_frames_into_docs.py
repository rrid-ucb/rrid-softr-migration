#!/usr/bin/env python3
"""
Integrate timestamped frames into markdown documentation files.

This script:
1. Creates a comprehensive linear walkthrough with all 168 frames integrated
2. Uses the linear file as a mapping reference to add frames to other documents
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_timestamp(timestamp_str: str) -> Optional[float]:
    """Convert timestamp string (HH:MM or HH:MM:SS) to seconds."""
    parts = timestamp_str.split(':')
    try:
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        pass
    return None


def load_frame_mapping(frames_timestamps_path: Path) -> Dict[str, str]:
    """Load frame mapping from timestamp log file."""
    with open(frames_timestamps_path) as f:
        frames_data = json.load(f)
    
    # Create mapping: timestamp -> filename
    mapping = {}
    for frame_info in frames_data:
        timestamp = frame_info['timestamp']
        filename = frame_info['filename']
        mapping[timestamp] = filename
    
    return mapping


def create_linear_walkthrough_with_frames(
    annotated_json_path: Path,
    frame_mapping: Dict[str, str],
    output_path: Path,
    frames_dir: Path
) -> Dict[str, str]:
    """
    Create a comprehensive linear walkthrough with all frames integrated.
    Returns a mapping of timestamp -> frame filename for use in other documents.
    """
    with open(annotated_json_path) as f:
        data = json.load(f)
    
    items = data.get("items", [])
    lines = []
    lines.append("# Complete Linear Walkthrough with Screenshots\n")
    lines.append("This document contains the complete transcript with screenshots for every segment.\n")
    
    # Track which timestamps we've seen to avoid duplicates
    seen_timestamps = set()
    timestamp_to_frame = {}
    
    current_chapter = None
    chapter_num = 0
    
    for i, item in enumerate(items):
        start_hms = item.get("start_hms", "")
        text = item.get("text", "").strip()
        
        if not text:
            continue
        
        # Get frame for this timestamp
        frame_filename = frame_mapping.get(start_hms)
        if not frame_filename:
            # Try to find closest frame
            start_seconds = item.get("start", 0)
            best_match = None
            min_diff = float('inf')
            
            for ts, fn in frame_mapping.items():
                ts_seconds = parse_timestamp(ts)
                if ts_seconds is not None:
                    diff = abs(ts_seconds - start_seconds)
                    if diff < min_diff and diff < 2.0:  # Within 2 seconds
                        min_diff = diff
                        best_match = fn
            
            if best_match:
                frame_filename = best_match
        
        # Add section header every ~20 segments or when there's a significant time gap
        if i == 0 or (i > 0 and items[i-1].get("start", 0) + 60 < item.get("start", 0)):
            chapter_num += 1
            minutes = int(item.get("start", 0) // 60)
            seconds = int(item.get("start", 0) % 60)
            lines.append(f"\n## Section {chapter_num}: {minutes:02d}:{seconds:02d}\n")
        
        # Add timestamp and text
        lines.append(f"**[{start_hms}]** {text}")
        
        # Add frame if we have one and haven't shown it recently
        if frame_filename and start_hms not in seen_timestamps:
            rel_path = f"../frames/{frame_filename}"
            lines.append(f"\n![Screenshot at {start_hms}]({rel_path})\n")
            seen_timestamps.add(start_hms)
            timestamp_to_frame[start_hms] = frame_filename
        
        lines.append("")  # Blank line between segments
    
    # Write the file
    output_path.write_text('\n'.join(lines))
    
    print(f"Created linear walkthrough with {len(seen_timestamps)} frames")
    return timestamp_to_frame


def find_timestamps_in_markdown(content: str) -> List[Tuple[str, int]]:
    """Find all timestamp references in markdown content. Returns list of (timestamp, line_number)."""
    timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
    timestamps = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        matches = timestamp_pattern.findall(line)
        for match in matches:
            timestamps.append((match, i))
    
    return timestamps


def add_frames_to_document(
    markdown_path: Path,
    frame_mapping: Dict[str, str],
    linear_timestamp_map: Dict[str, str],
    frames_dir: Path
) -> None:
    """
    Add frames to a markdown document based on timestamps.
    Uses linear_timestamp_map as the authoritative source for timestamp->frame mapping.
    Replaces old frame references with new timestamped ones.
    """
    content = markdown_path.read_text()
    lines = content.split('\n')
    result = []
    
    timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
    old_frame_pattern = re.compile(r'frame_\d+\.jpg')  # Pattern for old frame references
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for timestamp references
        matches = timestamp_pattern.findall(line)
        if matches:
            ts_str = matches[0]
            
            # Try to find frame from linear mapping first (most authoritative)
            frame_filename = linear_timestamp_map.get(ts_str)
            
            # If not found, try frame_mapping (from frames_timestamps.json)
            if not frame_filename:
                frame_filename = frame_mapping.get(ts_str)
            
            # If still not found, find closest match
            if not frame_filename:
                ts_seconds = parse_timestamp(ts_str)
                if ts_seconds is not None:
                    best_match = None
                    min_diff = float('inf')
                    
                    # Search in linear mapping first
                    for mapped_ts, frame_file in linear_timestamp_map.items():
                        mapped_seconds = parse_timestamp(mapped_ts)
                        if mapped_seconds is not None:
                            diff = abs(mapped_seconds - ts_seconds)
                            if diff < min_diff and diff < 5.0:  # Within 5 seconds
                                min_diff = diff
                                best_match = frame_file
                    
                    # If not found, search in frame_mapping
                    if not best_match:
                        for mapped_ts, frame_file in frame_mapping.items():
                            mapped_seconds = parse_timestamp(mapped_ts)
                            if mapped_seconds is not None:
                                diff = abs(mapped_seconds - ts_seconds)
                                if diff < min_diff and diff < 5.0:
                                    min_diff = diff
                                    best_match = frame_file
                    
                    if best_match:
                        frame_filename = best_match
            
            # Add the line with timestamp
            result.append(line)
            
            # Check if next few lines have an image that should be replaced
            image_found = False
            skip_lines = 0
            
            for j in range(1, 4):  # Check next 3 lines
                if i + j < len(lines):
                    next_line = lines[i + j]
                    
                    # If it's an image line, replace it
                    if next_line.strip().startswith('!['):
                        # Replace old frame reference with new one
                        if frame_filename:
                            rel_path = f"../frames/{frame_filename}"
                            result.append(f"![Screenshot at {ts_str}]({rel_path})")
                            skip_lines = j
                            image_found = True
                        break
                    elif next_line.strip() and not next_line.strip().startswith('-') and not next_line.strip().startswith('*'):
                        # Non-empty line that's not a list item - probably not related
                        break
            
            # If no image found, add one
            if not image_found and frame_filename:
                rel_path = f"../frames/{frame_filename}"
                result.append(f"![Screenshot at {ts_str}]({rel_path})")
            
            # Skip the lines we've already processed
            i += skip_lines + 1
        else:
            # Check if this line has an old frame reference that should be removed
            # (if it's not associated with a timestamp)
            if old_frame_pattern.search(line) and not timestamp_pattern.search(line):
                # Skip old frame references that aren't near a timestamp
                i += 1
                continue
            else:
                result.append(line)
                i += 1
    
    # Write updated content
    markdown_path.write_text('\n'.join(result))


def main():
    parser = argparse.ArgumentParser(
        description="Integrate frames into markdown documentation files"
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
        "--llm-docs-dir",
        default="out/llm_docs",
        help="Directory containing LLM-generated markdown files"
    )
    parser.add_argument(
        "--linear-output",
        default="out/llm_docs/linear_walkthrough_complete.md",
        help="Output path for complete linear walkthrough"
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Update existing markdown files (personas, PRD) with frames"
    )
    
    args = parser.parse_args()
    
    annotated_json_path = Path(args.annotated_json)
    frames_timestamps_path = Path(args.frames_timestamps)
    frames_dir = Path(args.frames_dir)
    llm_docs_dir = Path(args.llm_docs_dir)
    linear_output_path = Path(args.linear_output)
    
    # Validate inputs
    if not annotated_json_path.exists():
        print(f"Error: Annotated JSON not found: {annotated_json_path}", file=sys.stderr)
        sys.exit(1)
    
    if not frames_timestamps_path.exists():
        print(f"Error: Frames timestamps file not found: {frames_timestamps_path}", file=sys.stderr)
        sys.exit(1)
    
    # Load frame mapping
    print("Loading frame mapping...")
    frame_mapping = load_frame_mapping(frames_timestamps_path)
    print(f"Loaded {len(frame_mapping)} frame mappings")
    
    # Create comprehensive linear walkthrough
    print(f"\nCreating comprehensive linear walkthrough...")
    linear_timestamp_map = create_linear_walkthrough_with_frames(
        annotated_json_path,
        frame_mapping,
        linear_output_path,
        frames_dir
    )
    print(f"Created: {linear_output_path}")
    
    # Update other markdown files if requested
    if args.update_existing:
        print(f"\nUpdating existing markdown files...")
        markdown_files = [
            llm_docs_dir / "personas_stories_openai.md",
            llm_docs_dir / "prd_document_openai.md",
            llm_docs_dir / "linear_walkthrough_openai.md"  # Also update the original linear file
        ]
        
        for md_file in markdown_files:
            if md_file.exists():
                print(f"  Updating {md_file.name}...")
                add_frames_to_document(
                    md_file,
                    frame_mapping,
                    linear_timestamp_map,
                    frames_dir
                )
            else:
                print(f"  Skipping {md_file.name} (not found)")
    
    print("\n✓ Complete!")


if __name__ == "__main__":
    main()

