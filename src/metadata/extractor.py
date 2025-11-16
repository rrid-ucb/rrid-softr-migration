"""
Extract metadata from video files including EXIF, creation time, and video properties.
"""

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


@dataclass
class VideoMetadata:
    """Video metadata information."""
    filename: str
    file_path: str
    file_size_bytes: int
    duration_seconds: float
    duration_formatted: str
    width: int
    height: int
    fps: float
    codec: str
    bitrate: int
    creation_time: Optional[str] = None
    modification_time: Optional[str] = None
    format_name: str = ""
    audio_codec: Optional[str] = None
    audio_sample_rate: Optional[int] = None
    audio_channels: Optional[int] = None


class MetadataExtractor:
    """Extract metadata from video files using ffprobe."""
    
    def __init__(self):
        self.ffprobe_path = self._find_ffprobe()
    
    def _find_ffprobe(self) -> str:
        """Find ffprobe executable."""
        try:
            result = subprocess.run(['which', 'ffprobe'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        
        # Try common locations
        for path in ['/usr/local/bin/ffprobe', '/opt/homebrew/bin/ffprobe']:
            if Path(path).exists():
                return path
        
        raise RuntimeError("ffprobe not found. Install ffmpeg: brew install ffmpeg")
    
    def extract(self, video_path: Path) -> VideoMetadata:
        """Extract comprehensive metadata from video file."""
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Get file stats
        stat = video_path.stat()
        file_size = stat.st_size
        modification_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        # Use ffprobe to get video properties
        cmd = [
            self.ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(video_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            probe_data = json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffprobe failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse ffprobe output: {e}")
        
        # Extract format info
        format_info = probe_data.get('format', {})
        duration = float(format_info.get('duration', 0))
        
        # Extract creation time from format tags
        creation_time = None
        tags = format_info.get('tags', {})
        for key in ['creation_time', 'creationdate', 'date', 'com.apple.quicktime.creationdate']:
            if key in tags:
                creation_time = tags[key]
                break
        
        # Find video stream
        video_stream = None
        audio_stream = None
        
        for stream in probe_data.get('streams', []):
            if stream.get('codec_type') == 'video' and video_stream is None:
                video_stream = stream
            elif stream.get('codec_type') == 'audio' and audio_stream is None:
                audio_stream = stream
        
        if not video_stream:
            raise RuntimeError("No video stream found in file")
        
        # Extract video properties
        width = int(video_stream.get('width', 0))
        height = int(video_stream.get('height', 0))
        fps_str = video_stream.get('r_frame_rate', '0/1')
        fps_parts = fps_str.split('/')
        fps = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 and fps_parts[1] != '0' else 0
        codec = video_stream.get('codec_name', 'unknown')
        bitrate = int(format_info.get('bit_rate', 0))
        
        # Extract audio properties if available
        audio_codec = None
        audio_sample_rate = None
        audio_channels = None
        
        if audio_stream:
            audio_codec = audio_stream.get('codec_name')
            audio_sample_rate = int(audio_stream.get('sample_rate', 0)) if audio_stream.get('sample_rate') else None
            audio_channels = int(audio_stream.get('channels', 0)) if audio_stream.get('channels') else None
        
        # Format duration
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        duration_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return VideoMetadata(
            filename=video_path.name,
            file_path=str(video_path.resolve()),
            file_size_bytes=file_size,
            duration_seconds=duration,
            duration_formatted=duration_formatted,
            width=width,
            height=height,
            fps=fps,
            codec=codec,
            bitrate=bitrate,
            creation_time=creation_time,
            modification_time=modification_time,
            format_name=format_info.get('format_name', ''),
            audio_codec=audio_codec,
            audio_sample_rate=audio_sample_rate,
            audio_channels=audio_channels,
        )
    
    def save_metadata(self, metadata: VideoMetadata, output_path: Path):
        """Save metadata to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

