"""
Enhanced frame extraction with blank frame detection, audio analysis, and transcript heuristics.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
try:
    from PIL import Image
    import numpy as np
    HAS_IMAGE_LIBS = True
except ImportError:
    HAS_IMAGE_LIBS = False
    Image = None
    np = None


def is_blank_frame(image_path: Path, threshold: float = 0.95) -> bool:
    """
    Detect if a frame is blank/black.
    
    Args:
        image_path: Path to image file
        threshold: Brightness threshold (0-1), frames darker than this are considered blank
    
    Returns:
        True if frame appears to be blank/black
    """
    if not HAS_IMAGE_LIBS:
        return False  # Can't check without PIL/numpy
    
    try:
        img = Image.open(image_path)
        # Convert to grayscale
        gray = img.convert('L')
        # Calculate average brightness
        pixels = np.array(gray)
        avg_brightness = np.mean(pixels) / 255.0
        
        return avg_brightness < threshold
    except Exception as e:
        print(f"Warning: Could not analyze frame {image_path}: {e}", file=sys.stderr)
        return False  # Assume not blank if we can't analyze


def extract_frame_at_timestamp(
    video_path: Path, 
    timestamp_seconds: float, 
    output_path: Path,
    check_blank: bool = True
) -> Tuple[bool, bool]:
    """
    Extract a single frame from video at specific timestamp using ffmpeg.
    
    Returns:
        (success, is_blank) tuple
    """
    try:
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
        
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if not output_path.exists():
            return False, False
        
        # Check if blank
        is_blank = False
        if check_blank:
            is_blank = is_blank_frame(output_path)
            if is_blank:
                # Delete blank frame
                output_path.unlink()
        
        return True, is_blank
        
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frame at {timestamp_seconds}s: {e.stderr}", file=sys.stderr)
        return False, False
    except Exception as e:
        print(f"Unexpected error extracting frame at {timestamp_seconds}s: {e}", file=sys.stderr)
        return False, False


def analyze_audio_activity(video_path: Path, timestamp: float, window_seconds: float = 2.0) -> float:
    """
    Analyze audio activity around a timestamp to determine if it's a good frame extraction point.
    
    Returns:
        Audio activity score (0-1), higher means more audio activity
    """
    try:
        start_time = max(0, timestamp - window_seconds / 2)
        duration = window_seconds
        
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-ss', str(start_time),
            '-t', str(duration),
            '-i', str(video_path),
            '-af', 'volumedetect',
            '-f', 'null',
            '-'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Parse volume detection output
        mean_volume = 0.0
        for line in result.stderr.split('\n'):
            if 'mean_volume:' in line:
                try:
                    mean_volume = float(line.split('mean_volume:')[1].split('dB')[0].strip())
                    break
                except (ValueError, IndexError):
                    pass
        
        # Normalize to 0-1 scale (assuming -60dB to 0dB range)
        activity_score = max(0, min(1, (mean_volume + 60) / 60))
        return activity_score
        
    except Exception as e:
        print(f"Warning: Could not analyze audio at {timestamp}s: {e}", file=sys.stderr)
        return 0.5  # Default moderate activity


def extract_frames_with_heuristics(
    video_path: Path,
    timestamps: List[Tuple[float, str]],  # List of (seconds, timestamp_string)
    frames_dir: Path,
    annotated_json_path: Optional[Path] = None,
    check_blank: bool = True,
    use_audio_analysis: bool = True,
    min_audio_activity: float = 0.3
) -> Dict[str, str]:
    """
    Extract frames with heuristics to avoid blank frames and prioritize good moments.
    
    Args:
        video_path: Path to video file
        timestamps: List of (seconds, timestamp_string) tuples
        frames_dir: Directory to save frames
        annotated_json_path: Optional path to annotated.json for transcript heuristics
        check_blank: Whether to check for and skip blank frames
        use_audio_analysis: Whether to use audio activity analysis
        min_audio_activity: Minimum audio activity score to extract frame
    
    Returns:
        Dict mapping timestamp_string -> frame_filename
    """
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Load transcript if available for heuristics
    transcript_segments = {}
    if annotated_json_path and annotated_json_path.exists():
        try:
            with open(annotated_json_path) as f:
                data = json.load(f)
                for item in data.get('items', []):
                    start_hms = item.get('start_hms', '')
                    if start_hms:
                        transcript_segments[start_hms] = {
                            'start': item.get('start', 0),
                            'text': item.get('text', ''),
                            'end': item.get('end', 0)
                        }
        except Exception as e:
            print(f"Warning: Could not load transcript: {e}", file=sys.stderr)
    
    frame_map = {}
    frame_counter = 1
    blank_count = 0
    skipped_audio_count = 0
    
    # Sort timestamps by seconds
    sorted_timestamps = sorted(timestamps, key=lambda x: x[0])
    
    for seconds, timestamp_str in sorted_timestamps:
        # Check audio activity if enabled
        if use_audio_analysis:
            audio_activity = analyze_audio_activity(video_path, seconds)
            if audio_activity < min_audio_activity:
                skipped_audio_count += 1
                # Try to find nearby timestamp with better audio
                # Look within ±5 seconds
                best_seconds = seconds
                best_activity = audio_activity
                
                for offset in [-3, -2, -1, 1, 2, 3]:
                    test_seconds = max(0, seconds + offset)
                    test_activity = analyze_audio_activity(video_path, test_seconds)
                    if test_activity > best_activity:
                        best_seconds = test_seconds
                        best_activity = test_activity
                
                if best_activity >= min_audio_activity:
                    seconds = best_seconds
                else:
                    continue  # Skip this frame entirely
        
        # Format timestamp for filename
        timestamp_safe = timestamp_str.replace(':', '-')
        frame_filename = f"frame_{frame_counter:05d}_{timestamp_safe}.jpg"
        frame_path = frames_dir / frame_filename
        
        # Extract frame
        success, is_blank = extract_frame_at_timestamp(
            video_path, seconds, frame_path, check_blank=check_blank
        )
        
        if success and not is_blank:
            frame_map[timestamp_str] = frame_filename
            frame_counter += 1
        elif is_blank:
            blank_count += 1
    
    print(f"Extracted {len(frame_map)} frames")
    if blank_count > 0:
        print(f"Skipped {blank_count} blank frames")
    if skipped_audio_count > 0:
        print(f"Skipped {skipped_audio_count} frames with low audio activity")
    
    return frame_map

