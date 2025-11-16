#!/usr/bin/env python3
"""
Extract frames from video at specific timestamps and update markdown documentation.

This script:
1. Parses timestamps from LLM-generated markdown docs
2. Extracts frames from the video at those timestamps
3. Updates the markdown files with correct screenshot references
"""

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Tuple, Dict, Optional, Any


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


def extract_timestamps_from_markdown(markdown_path: Path) -> Set[str]:
    """Extract all timestamp references from markdown files."""
    timestamps = set()
    
    # Pattern matches: [00:00], **[00:00]**, [00:00:00], etc.
    timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
    
    content = markdown_path.read_text()
    matches = timestamp_pattern.findall(content)
    timestamps.update(matches)
    
    return timestamps


def extract_timestamps_from_transcript(annotated_json_path: Path) -> List[Tuple[float, str]]:
    """Extract all timestamps from transcript segments."""
    with open(annotated_json_path) as f:
        data = json.load(f)
    
    timestamps = []
    for item in data.get("items", []):
        start_time = item.get("start", 0)
        start_hms = item.get("start_hms", "")
        timestamps.append((start_time, start_hms))
    
    return timestamps


def extract_frame_at_timestamp(video_path: Path, timestamp_seconds: float, output_path: Path) -> bool:
    """Extract a single frame from video at specific timestamp using ffmpeg."""
    try:
        # Use ffmpeg to extract frame at exact timestamp
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-ss', str(timestamp_seconds),
            '-i', str(video_path),
            '-vframes', '1',
            '-q:v', '2',  # High quality
            '-y',  # Overwrite if exists
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return output_path.exists()
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frame at {timestamp_seconds}s: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error extracting frame at {timestamp_seconds}s: {e}", file=sys.stderr)
        return False


def format_timestamp_for_filename(timestamp_str: str) -> str:
    """Convert timestamp string to filesystem-safe format (HH-MM-SS or MM-SS)."""
    # Replace colons with dashes for filesystem compatibility
    return timestamp_str.replace(':', '-')


def extract_frames_for_timestamps(
    video_path: Path,
    timestamps: Set[str],
    frames_dir: Path,
    annotated_json_path: Path,
    extract_all_segments: bool = False
) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    """
    Extract frames at specified timestamps.
    Returns:
        - dict mapping timestamp string to frame filename
        - list of frame metadata dicts for logging
    """
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Create mapping from timestamp string to seconds
    timestamp_to_seconds = {}
    for ts_str in timestamps:
        seconds = parse_timestamp(ts_str)
        if seconds is not None:
            timestamp_to_seconds[ts_str] = seconds
    
    # Optionally add all transcript segment timestamps
    if extract_all_segments:
        transcript_timestamps = extract_timestamps_from_transcript(annotated_json_path)
        for seconds, hms in transcript_timestamps:
            if hms not in timestamp_to_seconds:
                timestamp_to_seconds[hms] = seconds
    
    # Sort timestamps by seconds to extract in order
    sorted_ts_items = sorted(timestamp_to_seconds.items(), key=lambda x: x[1])
    
    # Extract frames
    frame_map = {}  # Maps timestamp string -> frame filename
    existing_frames = {}  # Maps seconds -> frame filename (to avoid duplicates)
    frame_counter = 1
    frame_log = []  # List of frame metadata for logging
    
    for ts_str, seconds in sorted_ts_items:
        # Check if we already extracted a frame at this time (within 0.5 seconds)
        frame_filename = None
        for existing_seconds, existing_frame in existing_frames.items():
            if abs(existing_seconds - seconds) < 0.5:
                frame_filename = existing_frame
                break
        
        if not frame_filename:
            # Extract new frame with timestamp in filename
            ts_safe = format_timestamp_for_filename(ts_str)
            frame_filename = f"frame_{frame_counter:05d}_{ts_safe}.jpg"
            frame_path = frames_dir / frame_filename
            
            if extract_frame_at_timestamp(video_path, seconds, frame_path):
                existing_frames[seconds] = frame_filename
                frame_log.append({
                    "frame_number": frame_counter,
                    "filename": frame_filename,
                    "timestamp": ts_str,
                    "timestamp_seconds": seconds
                })
                frame_counter += 1
            else:
                continue  # Skip if extraction failed
        
        # Map timestamp string to frame filename
        frame_map[ts_str] = frame_filename
    
    return frame_map, frame_log


def update_markdown_with_frames(
    markdown_path: Path,
    frame_map: Dict[str, str],
    frames_dir: Path
) -> bool:
    """Update markdown file to include screenshot references for timestamps."""
    content = markdown_path.read_text()
    lines = content.split('\n')
    result = []
    
    # Pattern to find timestamp references
    timestamp_pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)
        
        # Look for timestamp references
        matches = timestamp_pattern.findall(line)
        if matches:
            # Check if next few lines already have an image for this timestamp
            has_image = False
            for j in range(i + 1, min(i + 4, len(lines))):
                check_line = lines[j].strip()
                if check_line.startswith('![') and matches[0] in check_line:
                    has_image = True
                    break
            
            # Skip if image already exists
            if not has_image:
                
                # Get the first timestamp in the line
                ts_str = matches[0]
                
                # Try to find matching frame
                frame_filename = None
                
                # Direct match
                if ts_str in frame_map:
                    frame_filename = frame_map[ts_str]
                else:
                    # Try to find closest match
                    ts_seconds = parse_timestamp(ts_str)
                    if ts_seconds is not None:
                        best_match = None
                        min_diff = float('inf')
                        
                        for mapped_ts, frame_file in frame_map.items():
                            mapped_seconds = parse_timestamp(mapped_ts)
                            if mapped_seconds is not None:
                                diff = abs(mapped_seconds - ts_seconds)
                                if diff < min_diff and diff < 5.0:  # Within 5 seconds
                                    min_diff = diff
                                    best_match = frame_file
                        
                        if best_match:
                            frame_filename = best_match
                
                # Add screenshot reference
                if frame_filename:
                    # Calculate relative path from markdown to frames
                    # markdown is in out/llm_docs/, frames are in out/frames/
                    rel_path = f"../frames/{frame_filename}"
                    result.append(f"\n![Screenshot at {ts_str}]({rel_path})\n")
        
        i += 1
    
    # Write updated content
    markdown_path.write_text('\n'.join(result))
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames at timestamps and update markdown docs"
    )
    parser.add_argument(
        "video_path",
        help="Path to video file"
    )
    parser.add_argument(
        "--annotated-json",
        default="out/annotated.json",
        help="Path to annotated.json file"
    )
    parser.add_argument(
        "--frames-dir",
        default="out/frames",
        help="Directory to store extracted frames"
    )
    parser.add_argument(
        "--llm-docs-dir",
        default="out/llm_docs",
        help="Directory containing LLM-generated markdown files"
    )
    parser.add_argument(
        "--extract-all-segments",
        action="store_true",
        help="Extract frames for all transcript segments, not just referenced timestamps"
    )
    
    args = parser.parse_args()
    
    video_path = Path(args.video_path)
    annotated_json_path = Path(args.annotated_json)
    frames_dir = Path(args.frames_dir)
    llm_docs_dir = Path(args.llm_docs_dir)
    
    # Validate inputs
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)
    
    if not annotated_json_path.exists():
        print(f"Error: Annotated JSON not found: {annotated_json_path}", file=sys.stderr)
        sys.exit(1)
    
    # Find all markdown files in llm_docs directory
    markdown_files = list(llm_docs_dir.glob("*.md"))
    if not markdown_files:
        print(f"Warning: No markdown files found in {llm_docs_dir}", file=sys.stderr)
    
    # Extract timestamps from markdown files
    all_timestamps = set()
    for md_file in markdown_files:
        if md_file.name == "README.md":
            continue  # Skip README
        timestamps = extract_timestamps_from_markdown(md_file)
        all_timestamps.update(timestamps)
        print(f"Found {len(timestamps)} timestamps in {md_file.name}")
    
    print(f"\nTotal unique timestamps found in markdown: {len(all_timestamps)}")
    
    # If extract-all-segments, also get timestamps from transcript
    if args.extract_all_segments:
        transcript_timestamps = extract_timestamps_from_transcript(annotated_json_path)
        transcript_count = len(transcript_timestamps)
        print(f"Will also extract frames for {transcript_count} transcript segments")
    
    # Extract frames
    print(f"\nExtracting frames from {video_path}...")
    frame_map, frame_log = extract_frames_for_timestamps(
        video_path,
        all_timestamps,
        frames_dir,
        annotated_json_path,
        extract_all_segments=args.extract_all_segments
    )
    
    print(f"Extracted {len(frame_log)} unique frames")
    
    # Generate timestamp log file
    timestamp_log_path = frames_dir / "frames_timestamps.json"
    with open(timestamp_log_path, 'w') as f:
        json.dump(frame_log, f, indent=2)
    print(f"  Generated timestamp log: {timestamp_log_path}")
    
    # Also generate a CSV version for easy viewing
    import csv
    csv_log_path = frames_dir / "frames_timestamps.csv"
    with open(csv_log_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["frame_number", "filename", "timestamp", "timestamp_seconds"])
        writer.writeheader()
        writer.writerows(frame_log)
    print(f"  Generated CSV log: {csv_log_path}")
    
    # Update markdown files
    print(f"\nUpdating markdown files...")
    for md_file in markdown_files:
        if md_file.name == "README.md":
            continue  # Skip README
        print(f"  Updating {md_file.name}...")
        update_markdown_with_frames(md_file, frame_map, frames_dir)
    
    print("\n✓ Complete!")
    print(f"  Frames extracted to: {frames_dir}")
    print(f"  Timestamp logs: {timestamp_log_path.name}, {csv_log_path.name}")
    print(f"  Updated markdown files in: {llm_docs_dir}")


if __name__ == "__main__":
    main()

