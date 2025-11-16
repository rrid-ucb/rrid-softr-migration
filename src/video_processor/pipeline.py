"""
Main video processing pipeline that orchestrates all steps.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..config.manager import ConfigManager
from ..metadata.extractor import MetadataExtractor, VideoMetadata
from ..frame_extraction.extractor import extract_frames_with_heuristics


class VideoProcessor:
    """Process videos through the complete annotation pipeline."""
    
    def __init__(self, config_manager: ConfigManager, output_base: Path):
        self.config = config_manager
        self.output_base = Path(output_base)
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.metadata_extractor = MetadataExtractor()
    
    def process_video(
        self,
        video_path: Path,
        timestamped: bool = True,
        extract_all_frames: bool = True
    ) -> Path:
        """
        Process a single video through the complete pipeline.
        
        Returns:
            Path to the output directory for this video
        """
        video_path = Path(video_path)
        video_name = video_path.stem
        
        # Create output directory structure
        if timestamped:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.output_base / video_name / timestamp
        else:
            output_dir = self.output_base / video_name
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Processing: {video_path.name}")
        print(f"Output: {output_dir}")
        print(f"{'='*60}\n")
        
        # Step 1: Extract metadata
        print("[1/5] Extracting video metadata...")
        try:
            metadata = self.metadata_extractor.extract(video_path)
            metadata_path = output_dir / 'metadata.json'
            self.metadata_extractor.save_metadata(metadata, metadata_path)
            print(f"  ✓ Duration: {metadata.duration_formatted}")
            print(f"  ✓ Resolution: {metadata.width}x{metadata.height}")
            print(f"  ✓ Created: {metadata.creation_time or 'Unknown'}")
        except Exception as e:
            print(f"  ✗ Error extracting metadata: {e}")
            metadata = None
        
        # Step 2: Transcribe
        print("\n[2/5] Transcribing video...")
        transcript_path = output_dir / f"{video_name}.json"
        whisper_model = self.config.get_model('transcription')
        if not whisper_model:
            whisper_model = {'name': 'base'}  # Default
        
        try:
            self._transcribe_video(video_path, transcript_path, whisper_model['name'])
            print(f"  ✓ Transcript saved: {transcript_path}")
        except Exception as e:
            print(f"  ✗ Transcription failed: {e}")
            return output_dir
        
        # Step 3: Extract frames
        print("\n[3/5] Extracting frames...")
        frames_dir = output_dir / 'frames'
        
        try:
            # Load transcript to get timestamps
            with open(transcript_path) as f:
                transcript_data = json.load(f)
            
            timestamps = []
            for item in transcript_data.get('segments', []):
                start = item.get('start', 0)
                start_hms = self._seconds_to_hms(start)
                timestamps.append((start, start_hms))
            
            # Extract frames with heuristics
            frame_map = extract_frames_with_heuristics(
                video_path,
                timestamps,
                frames_dir,
                annotated_json_path=None,  # Will be created in next step
                check_blank=True,
                use_audio_analysis=True
            )
            
            # Save frame mapping
            frames_log = frames_dir / 'frames_timestamps.json'
            frame_log_data = []
            for ts_str, filename in frame_map.items():
                # Find corresponding seconds
                seconds = next((s for s, hms in timestamps if hms == ts_str), 0)
                frame_log_data.append({
                    'timestamp': ts_str,
                    'timestamp_seconds': seconds,
                    'filename': filename
                })
            
            with open(frames_log, 'w') as f:
                json.dump(frame_log_data, f, indent=2)
            
            print(f"  ✓ Extracted {len(frame_map)} frames")
            
        except Exception as e:
            print(f"  ✗ Frame extraction failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 4: Create annotated transcript
        print("\n[4/5] Creating annotated transcript...")
        annotated_path = output_dir / 'annotated.json'
        try:
            self._create_annotated_transcript(
                video_path, transcript_path, frames_dir, annotated_path
            )
            print(f"  ✓ Annotated transcript: {annotated_path}")
        except Exception as e:
            print(f"  ✗ Annotation failed: {e}")
        
        # Step 5: Generate LLM documentation
        print("\n[5/5] Generating LLM documentation...")
        llm_docs_dir = output_dir / 'llm_docs'
        try:
            from ..llm.generator import LLMDocumentGenerator
            generator = LLMDocumentGenerator(self.config)
            generator.generate_documents(annotated_path, frames_dir, llm_docs_dir)
            print(f"  ✓ LLM docs generated in: {llm_docs_dir}")
        except Exception as e:
            print(f"  ✗ LLM generation failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 6: Generate HTML browser
        print("\n[6/6] Generating HTML browser...")
        try:
            from ..output_generator.html_browser import HTMLBrowserGenerator
            browser_gen = HTMLBrowserGenerator(self.output_base)
            index_path = browser_gen.generate_html_browser()
            print(f"  ✓ HTML browser: {index_path}")
        except Exception as e:
            print(f"  ⚠ HTML browser generation failed: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\n✓ Complete! Output: {output_dir}")
        return output_dir
    
    def _transcribe_video(self, video_path: Path, output_path: Path, model: str):
        """Transcribe video using Whisper."""
        cmd = [
            'whisper',
            str(video_path),
            '--model', model,
            '--language', 'en',
            '--output_format', 'json',
            '--output_dir', str(output_path.parent)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Whisper failed: {result.stderr}")
    
    def _seconds_to_hms(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS or MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def _create_annotated_transcript(
        self,
        video_path: Path,
        transcript_path: Path,
        frames_dir: Path,
        output_path: Path
    ):
        """Create annotated transcript linking transcript segments to frames."""
        # This is a simplified version - the full annotate_video.py logic would go here
        # For now, create basic structure
        with open(transcript_path) as f:
            transcript_data = json.load(f)
        
        annotated = {
            'video': str(video_path),
            'transcript': str(transcript_path),
            'frames_dir': str(frames_dir),
            'items': []
        }
        
        # Load frame mapping
        frames_log = frames_dir / 'frames_timestamps.json'
        frame_map = {}
        if frames_log.exists():
            with open(frames_log) as f:
                frame_data = json.load(f)
                frame_map = {item['timestamp']: item['filename'] for item in frame_data}
        
        for segment in transcript_data.get('segments', []):
            start = segment.get('start', 0)
            end = segment.get('end', 0)
            text = segment.get('text', '')
            start_hms = self._seconds_to_hms(start)
            
            # Find matching frame
            frame_filename = frame_map.get(start_hms)
            frame_info = None
            if frame_filename:
                frame_info = {
                    'path': str(frames_dir / frame_filename),
                    'time': start
                }
            
            annotated['items'].append({
                'start': start,
                'end': end,
                'start_hms': start_hms,
                'end_hms': self._seconds_to_hms(end),
                'text': text,
                'frame': frame_info or {}
            })
        
        with open(output_path, 'w') as f:
            json.dump(annotated, f, indent=2)
    
    def process_directory(self, input_dir: Path, pattern: str = "*.mp4"):
        """Process all videos in a directory."""
        input_dir = Path(input_dir)
        videos = list(input_dir.glob(pattern))
        
        if not videos:
            print(f"No videos found in {input_dir} matching {pattern}")
            return
        
        print(f"Found {len(videos)} video(s) to process\n")
        
        for video in videos:
            try:
                self.process_video(video)
            except Exception as e:
                print(f"\n✗ Failed to process {video.name}: {e}")
                import traceback
                traceback.print_exc()

