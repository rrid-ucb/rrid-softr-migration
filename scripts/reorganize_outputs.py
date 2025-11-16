#!/usr/bin/env python3
"""
Reorganize output directory into run-based structure.

Moves from:
  out/
    llm_docs/
    llm_docs_enriched/
    frames/
    annotated.json

To:
  output/
    {video_name}/
      {run_timestamp}/
        frames/
        transcripts/
        docs/
          {model}/
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def get_video_name_from_files(files):
    """Determine video name from files."""
    # Look for softr.json or similar
    for f in files:
        path_str = str(f["path"])
        if path_str.endswith(".json") and "softr" in path_str.lower():
            return "softr"
    # Default
    return "unknown"


def group_files_by_run(files, time_window_minutes=10):
    """Group files by run time."""
    runs = defaultdict(list)
    
    for f in files:
        mtime = f["mtime"]
        # Round to nearest time window
        minutes = (mtime.minute // time_window_minutes) * time_window_minutes
        rounded_time = mtime.replace(minute=minutes, second=0, microsecond=0)
        run_key = rounded_time.strftime("%Y%m%d_%H%M%S")
        runs[run_key].append(f)
    
    return runs


def reorganize_outputs():
    """Reorganize out/ to output/ with run-based structure."""
    out_dir = Path("out")
    output_dir = Path("output")
    
    if not out_dir.exists():
        print("No 'out' directory found")
        return
    
    # Collect all files
    files_info = []
    for file_path in out_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            stat = file_path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            rel_path = file_path.relative_to(out_dir)
            files_info.append({
                "path": rel_path,
                "full_path": file_path,
                "mtime": mtime,
                "size": stat.st_size
            })
    
    if not files_info:
        print("No files found in 'out' directory")
        return
    
    # Group by runs
    runs = group_files_by_run(files_info)
    
    print(f"Found {len(runs)} run(s)")
    
    # Determine video name
    video_name = get_video_name_from_files(files_info)
    print(f"Video name: {video_name}")
    
    # Reorganize
    for run_key, run_files in sorted(runs.items()):
        run_dir = output_dir / video_name / run_key
        
        print(f"\nProcessing run: {run_key}")
        print(f"  Output: {run_dir}")
        
        # Categorize files
        frames = []
        transcripts = []
        docs = defaultdict(list)
        
        for f in run_files:
            path_str = str(f["path"])
            
            if "frames" in path_str.lower() or path_str.endswith(".jpg"):
                frames.append(f)
            elif path_str.endswith(".json") and ("annotated" in path_str or "softr" in path_str):
                transcripts.append(f)
            elif path_str.endswith(".md") or ("llm_docs" in path_str.lower()):
                # Determine model from path
                if "enriched" in path_str.lower():
                    model = "gemini_vision"
                elif "openai" in path_str.lower():
                    model = "openai"
                elif "gemini" in path_str.lower():
                    model = "gemini"
                else:
                    model = "unknown"
                docs[model].append(f)
            else:
                transcripts.append(f)  # Default to transcripts
        
        # Create directories
        frames_dir = run_dir / "frames"
        transcripts_dir = run_dir / "transcripts"
        docs_dir = run_dir / "docs"
        
        frames_dir.mkdir(parents=True, exist_ok=True)
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Move frames
        for f in frames:
            dest = frames_dir / f["path"].name
            if f["full_path"].exists():
                shutil.copy2(f["full_path"], dest)
                print(f"  Copied frame: {f['path'].name}")
        
        # Move transcripts
        for f in transcripts:
            dest = transcripts_dir / f["path"].name
            if f["full_path"].exists():
                shutil.copy2(f["full_path"], dest)
                print(f"  Copied transcript: {f['path'].name}")
        
        # Move docs (remove "enriched" from filenames)
        for model, model_files in docs.items():
            model_dir = docs_dir / model
            model_dir.mkdir(parents=True, exist_ok=True)
            
            for f in model_files:
                # Remove "enriched" and model suffix, keep base name
                old_name = f["path"].name
                new_name = old_name.replace("_enriched", "")
                new_name = new_name.replace("_openai", "")
                new_name = new_name.replace("_gemini", "")
                new_name = new_name.replace("_complete", "")
                
                # Ensure .md extension
                if not new_name.endswith(".md"):
                    new_name = new_name.replace(".txt", ".md")
                
                dest = model_dir / new_name
                if f["full_path"].exists():
                    shutil.copy2(f["full_path"], dest)
                    print(f"  Copied doc ({model}): {new_name}")
        
        # Create run metadata
        metadata = {
            "run_timestamp": run_key,
            "video_name": video_name,
            "files": {
                "frames": len(frames),
                "transcripts": len(transcripts),
                "docs": {model: len(files) for model, files in docs.items()}
            }
        }
        
        metadata_path = run_dir / "run_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"  Created metadata: {metadata_path}")
    
    print(f"\n✓ Reorganization complete!")
    print(f"  Old location: {out_dir}")
    print(f"  New location: {output_dir}")
    print(f"\n  You can now remove 'out' directory if desired")


if __name__ == "__main__":
    reorganize_outputs()

