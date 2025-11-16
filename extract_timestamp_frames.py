#!/usr/bin/env python3
"""
Extract frames at specific timestamps referenced in LLM-generated markdown docs.

This script:
1. Parses timestamps from markdown files in out/llm_docs/
2. Extracts frames at those timestamps from the video
3. Updates the markdown files to reference the correct frames

Usage:
    python3 extract_timestamp_frames.py <video_file> [--llm-docs-dir out/llm_docs] [--frames-dir out/frames]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Set, Tuple, List, Dict


def parse_timestamp(timestamp_str: str) -> float:
    """
    Parse timestamp string (HH:MM:SS or MM:SS) to seconds.
    
    Examples:
        "00:00" -> 0.0
        "01:23" -> 83.0
        "21:37" -> 1297.0
        "1:05:30" -> 3930.0
    """
    parts = timestamp_str.split(':')
    if len(parts) == 2:
        # MM:SS format
        minutes, seconds = int(parts[0]), int(parts[1])
        return minutes * 60 + seconds
    elif len(parts) == 3:
        # HH:MM:SS format
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}")


def find_timestamps_in_markdown(markdown_path: Path) -> Set[str]:
    """
    Extract all timestamp references from a markdown file.
    
    Matches patterns like:
    - [00:00]
    - **[00:47]**
    - [01:06]
    - [21:37]
    - [1:05:30]
    """
    content = markdown_path.read_text()
    
    # Pattern matches: [MM:SS] or [HH:MM:SS] with optional bold markers
    # Matches: [00:00], **[00:47]**, [01:06], [21:37], [1:05:30]
    timestamp_pattern = re.compile(r'\*?\[(\d{1,2}:\d{2}(?::\d{2})?)\]\*?')
    
    timestamps = set()
    for match in timestamp_pattern.finditer(content):
        timestamp_str = match.group(1)
        timestamps.add(timestamp_str)
    
    return timestamps


def extract_frame_at_timestamp(video_path: Path, timestamp: float, output_path: Path) -> bool:
    """
    Extract a single frame at a specific timestamp using ffmpeg.
    
    Returns True if successful, False otherwise.
    """
    try:
        # Use ffmpeg to extract frame at exact timestamp
        # -ss: seek to timestamp
        # -vframes 1: extract only 1 frame
        # -q:v 2: high quality JPEG
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-ss', str(timestamp),
            '-i', str(video_path),
            '-vframes', '1',
            '-q:v', '2',
            '-y',  # Overwrite if exists
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return output_path.exists()
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frame at {timestamp}s: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error extracting frame at {timestamp}s: {e}", file=sys.stderr)
        return False


def get_next_frame_number(frames_dir: Path) -> int:
    """Get the next available frame number."""
    existing_frames = sorted(frames_dir.glob("frame_*.jpg"))
    if not existing_frames:
        return 1
    
    # Extract number from last frame filename
    last_frame = existing_frames[-1]
    match = re.search(r'frame_(\d+)\.jpg', last_frame.name)
    if match:
        return int(match.group(1)) + 1
    
    return len(existing_frames) + 1


def update_markdown_with_frames(markdown_path: Path, timestamp_to_frame: Dict[str, str]) -> bool:
    """
    Update markdown file to reference the correct frames for each timestamp.
    
    Replaces existing image references or adds new ones after timestamp mentions.
    """
    content = markdown_path.read_text()
    lines = content.split('\n')
    result = []
    
    # Pattern to match timestamps
    timestamp_pattern = re.compile(r'(\*?)\[(\d{1,2}:\d{2}(?::\d{2})?)\]\*?')
    # Pattern to match image references
    image_pattern = re.compile(r'!\[.*?\]\(([^)]+)\)')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line contains a timestamp
        matches = list(timestamp_pattern.finditer(line))
        if matches:
            # Get the first timestamp in the line
            timestamp_str = matches[0].group(2)
            
            if timestamp_str in timestamp_to_frame:
                frame_filename = timestamp_to_frame[timestamp_str]
                rel_path = f"../frames/{frame_filename}"
                
                # Add the line with timestamp
                result.append(line)
                
                # Check if next few lines have an image that should be replaced
                image_found = False
                skip_lines = 0
                
                for j in range(1, 4):  # Check next 3 lines
                    if i + j < len(lines):
                        next_line = lines[i + j]
                        
                        # If it's an image line, check if it's for this timestamp
                        if next_line.strip().startswith('!['):
                            # Check if this image is associated with our timestamp
                            # (either contains the timestamp in the alt text or is right after the timestamp line)
                            if timestamp_str in next_line:
                                # Replace this image with the correct one
                                result.append(f"![Screenshot at {timestamp_str}]({rel_path})")
                                skip_lines = j
                                image_found = True
                                break
                            else:
                                # Different timestamp's image, don't replace
                                break
                        elif next_line.strip() and not next_line.strip().startswith('-'):
                            # Non-empty line that's not a list item - probably not related
                            break
                
                # If no image found, add one
                if not image_found:
                    # Add blank line if needed
                    if result and result[-1].strip() and not result[-1].strip().endswith(':'):
                        result.append("")
                    result.append(f"![Screenshot at {timestamp_str}]({rel_path})")
                
                # Skip lines we've already processed
                i += skip_lines + 1
                continue
        
        # Regular line - just add it
        result.append(line)
        i += 1
    
    # Write updated content
    updated_content = '\n'.join(result)
    markdown_path.write_text(updated_content)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames at timestamps referenced in LLM-generated markdown docs"
    )
    parser.add_argument(
        "video_file",
        help="Path to video file"
    )
    parser.add_argument(
        "--llm-docs-dir",
        default="out/llm_docs",
        help="Directory containing LLM-generated markdown files (default: out/llm_docs)"
    )
    parser.add_argument(
        "--frames-dir",
        default="out/frames",
        help="Directory to store extracted frames (default: out/frames)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be extracted without actually extracting frames"
    )
    
    args = parser.parse_args()
    
    video_path = Path(args.video_file)
    llm_docs_dir = Path(args.llm_docs_dir)
    frames_dir = Path(args.frames_dir)
    
    # Validate inputs
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)
    
    if not llm_docs_dir.exists():
        print(f"Error: LLM docs directory not found: {llm_docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Create frames directory if it doesn't exist
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all markdown files
    markdown_files = list(llm_docs_dir.glob("*.md"))
    if not markdown_files:
        print(f"Warning: No markdown files found in {llm_docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Collect all unique timestamps from all markdown files
    print("Parsing timestamps from markdown files...")
    all_timestamps = set()
    for md_file in markdown_files:
        timestamps = find_timestamps_in_markdown(md_file)
        all_timestamps.update(timestamps)
        print(f"  {md_file.name}: {len(timestamps)} timestamps")
    
    print(f"\nFound {len(all_timestamps)} unique timestamps")
    
    # Convert timestamps to seconds and sort
    timestamp_seconds = []
    for ts_str in sorted(all_timestamps):
        try:
            seconds = parse_timestamp(ts_str)
            timestamp_seconds.append((ts_str, seconds))
        except ValueError as e:
            print(f"Warning: Skipping invalid timestamp '{ts_str}': {e}", file=sys.stderr)
    
    print(f"Extracting {len(timestamp_seconds)} frames...")
    
    # Map timestamp strings to frame filenames
    timestamp_to_frame = {}
    next_frame_num = get_next_frame_number(frames_dir)
    
    extracted_count = 0
    skipped_count = 0
    
    for ts_str, seconds in timestamp_seconds:
        frame_filename = f"frame_{next_frame_num:05d}.jpg"
        frame_path = frames_dir / frame_filename
        
        # Check if frame already exists (might have been extracted before)
        if frame_path.exists():
            print(f"  [{ts_str}] Frame already exists: {frame_filename}")
            timestamp_to_frame[ts_str] = frame_filename
            skipped_count += 1
        else:
            if args.dry_run:
                print(f"  [{ts_str}] Would extract: {frame_filename} (at {seconds:.2f}s)")
                timestamp_to_frame[ts_str] = frame_filename
            else:
                print(f"  [{ts_str}] Extracting frame at {seconds:.2f}s -> {frame_filename}...", end=" ")
                if extract_frame_at_timestamp(video_path, seconds, frame_path):
                    print("✓")
                    timestamp_to_frame[ts_str] = frame_filename
                    extracted_count += 1
                else:
                    print("✗ Failed")
                    skipped_count += 1
        
        next_frame_num += 1
    
    print(f"\nExtraction complete:")
    print(f"  Extracted: {extracted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total frames: {len(timestamp_to_frame)}")
    
    if args.dry_run:
        print("\nDry run mode - no frames extracted, no files updated")
        return
    
    # Update markdown files with frame references
    print(f"\nUpdating markdown files...")
    for md_file in markdown_files:
        print(f"  Updating {md_file.name}...", end=" ")
        if update_markdown_with_frames(md_file, timestamp_to_frame):
            print("✓")
        else:
            print("✗ Failed")
    
    print("\n✓ Complete!")
    print(f"\nFrames directory: {frames_dir}")
    print(f"Updated markdown files: {len(markdown_files)}")


if __name__ == "__main__":
    main()

