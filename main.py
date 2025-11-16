#!/usr/bin/env python3
"""
Main entry point for video annotation system.

Usage:
    python main.py --configure                    # Configure system
    python main.py --process video.mp4            # Process single video
    python main.py --process-all input/           # Process all videos in directory
    python main.py --list-models                  # List available models
"""

import argparse
import sys
from pathlib import Path

from src.config.manager import ConfigManager
from src.video_processor.pipeline import VideoProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Video Annotation System - Generate comprehensive documentation from video walkthroughs"
    )
    
    parser.add_argument(
        '--configure',
        action='store_true',
        help='Run interactive configuration'
    )
    
    parser.add_argument(
        '--process',
        type=str,
        help='Process a single video file'
    )
    
    parser.add_argument(
        '--process-all',
        type=str,
        help='Process all videos in a directory'
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        default='input',
        help='Input directory for videos (default: input)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--no-timestamp',
        action='store_true',
        help='Do not use timestamped output directories'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List all available models'
    )
    
    parser.add_argument(
        '--config-dir',
        type=str,
        help='Custom configuration directory'
    )
    
    args = parser.parse_args()
    
    # Initialize config manager
    config_dir = Path(args.config_dir) if args.config_dir else None
    config_manager = ConfigManager(config_dir)
    
    # Handle configuration
    if args.configure:
        config_manager.configure(interactive=True)
        print("\n✓ Configuration complete!")
        return
    
    # Handle list models
    if args.list_models:
        model_discovery = config_manager.model_discovery
        print("\nAvailable Models:")
        print("=" * 60)
        
        for task_type in ['transcription', 'vision', 'general', 'thinking']:
            print(f"\n{task_type.upper()}:")
            models = model_discovery.get_recommended_models(task_type, 'balanced')
            for model in models[:10]:
                print(f"  - {model.provider.upper()}: {model.name}")
                print(f"    Speed: {model.speed_tier}, Cost: {model.cost_tier}")
                print(f"    {model.description}")
        return
    
    # Check if configured
    if not config_manager.is_configured():
        print("\n⚠ System not configured. Running configuration...")
        config_manager.configure(interactive=True)
        print("\n✓ Configuration complete! You can now process videos.")
        return
    
    # Initialize processor
    output_base = Path(args.output_dir)
    processor = VideoProcessor(config_manager, output_base)
    
    # Process videos
    if args.process:
        video_path = Path(args.process)
        if not video_path.exists():
            print(f"Error: Video file not found: {video_path}")
            sys.exit(1)
        
        processor.process_video(video_path, timestamped=not args.no_timestamp)
    
    elif args.process_all:
        input_dir = Path(args.process_all)
        if not input_dir.exists():
            print(f"Error: Input directory not found: {input_dir}")
            sys.exit(1)
        
        processor.process_directory(input_dir)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

