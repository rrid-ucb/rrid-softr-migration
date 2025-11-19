"""
VTT transcript parser to convert VTT files to Whisper JSON format.
Handles WebVTT format used by Zoom and other video platforms.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_vtt_time(time_str: str) -> float:
    """
    Parse VTT timestamp (HH:MM:SS.mmm) to seconds.
    
    Examples:
        "00:00:15.040" -> 15.04
        "01:23:45.678" -> 5025.678
    """
    parts = time_str.split(':')
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return 0.0


def parse_vtt_to_whisper_json(vtt_path: Path) -> Dict:
    """
    Parse a WebVTT file and convert to Whisper JSON format.
    
    Args:
        vtt_path: Path to .vtt file
        
    Returns:
        Dictionary in Whisper JSON format with 'segments' list
    """
    content = vtt_path.read_text(encoding='utf-8')
    
    # Remove WEBVTT header if present
    content = re.sub(r'^WEBVTT\s*\n', '', content, flags=re.MULTILINE)
    
    segments = []
    segment_id = 0
    
    # Pattern to match VTT cue blocks:
    # Number
    # HH:MM:SS.mmm --> HH:MM:SS.mmm
    # Text content (may span multiple lines)
    # (blank line)
    pattern = re.compile(
        r'(\d+)\s*\n'  # Cue number
        r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n'  # Timestamps
        r'(.+?)(?=\n\d+\s*\n|\Z)',  # Text content (non-greedy until next cue or end)
        re.DOTALL | re.MULTILINE
    )
    
    matches = pattern.finditer(content)
    
    for match in matches:
        cue_num = match.group(1)
        start_time_str = match.group(2)
        end_time_str = match.group(3)
        text = match.group(4).strip()
        
        # Remove speaker labels if present (e.g., "Rrid SP_Account: ")
        text = re.sub(r'^[^:]+:\s*', '', text)
        
        # Clean up text (remove extra whitespace, newlines)
        text = ' '.join(text.split())
        
        if text:  # Only add non-empty segments
            start = parse_vtt_time(start_time_str)
            end = parse_vtt_time(end_time_str)
            
            segments.append({
                'id': segment_id,
                'start': start,
                'end': end,
                'text': text
            })
            segment_id += 1
    
    return {
        'segments': segments,
        'text': ' '.join([seg['text'] for seg in segments])
    }


def find_transcript_file(video_path: Path) -> Optional[Path]:
    """
    Find an existing transcript file for a video.
    
    Looks for common transcript file patterns:
    - {video_name}.transcript.vtt
    - {video_name}.cc.vtt
    - {video_name}.vtt
    - {video_name}_transcript.txt
    - Transcript.txt (in same directory)
    
    Args:
        video_path: Path to video file
        
    Returns:
        Path to transcript file if found, None otherwise
    """
    video_dir = video_path.parent
    video_stem = video_path.stem
    
    # Common patterns for Zoom/recording transcripts
    patterns = [
        # Zoom patterns
        f"{video_stem}.transcript.vtt",
        f"{video_stem}.cc.vtt",
        f"{video_stem}.vtt",
        # Generic patterns
        f"{video_stem}_transcript.txt",
        f"{video_stem}_transcript.vtt",
        "Transcript.txt",
        "transcript.txt",
        "*.transcript.vtt",  # Wildcard pattern
        "*.cc.vtt",  # Wildcard pattern
    ]
    
    # Check exact matches first
    for pattern in patterns[:7]:  # First 7 are exact patterns
        candidate = video_dir / pattern
        if candidate.exists() and candidate.is_file():
            return candidate
    
    # Check wildcard patterns
    for pattern in patterns[7:]:
        matches = list(video_dir.glob(pattern))
        if matches:
            # Prefer files with similar name to video
            for match in matches:
                if video_stem.lower() in match.stem.lower():
                    return match
            # Otherwise return first match
            return matches[0]
    
    # Also check parent directory (for nested structures like Zoom recordings)
    # This handles cases like: video_dir/VIDEO_NAME/Recording.mp4 with transcript in video_dir/
    parent_dir = video_dir.parent
    for pattern in patterns[:7]:
        candidate = parent_dir / pattern
        if candidate.exists() and candidate.is_file():
            return candidate
    
    # Check for common transcript filenames in parent directory (Zoom often puts transcripts there)
    common_names = [
        "Transcript.txt",
        "transcript.txt",
        "Airtable_Automations_Walkthrough_Transcript.txt",  # Specific to this project
    ]
    for name in common_names:
        candidate = parent_dir / name
        if candidate.exists() and candidate.is_file():
            return candidate
    
    return None


def detect_transcript_type(transcript_path: Path) -> str:
    """
    Detect the type of transcript file.
    
    Returns:
        'vtt', 'txt', or 'json'
    """
    suffix = transcript_path.suffix.lower()
    if suffix == '.vtt':
        return 'vtt'
    elif suffix == '.txt':
        return 'txt'
    elif suffix == '.json':
        return 'json'
    else:
        # Try to detect by content
        content = transcript_path.read_text(encoding='utf-8', errors='ignore')[:100]
        if 'WEBVTT' in content or '-->' in content:
            return 'vtt'
        elif '{' in content and '"segments"' in content:
            return 'json'
        else:
            return 'txt'

