#!/usr/bin/env python3
"""
Create a comprehensive mapping file showing where each out/ file went in output/.
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict


def file_hash(file_path):
    """Calculate MD5 hash of file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_mapping():
    """Create comprehensive file mapping."""
    out_dir = Path("out")
    output_dir = Path("output")
    
    if not out_dir.exists():
        print("No 'out' directory found")
        return
    
    mapping = {
        "summary": {},
        "files": []
    }
    
    # Known mappings for renamed files
    renamed_mappings = {
        "llm_docs/linear_walkthrough_openai.md": "softr/20251116_003000/docs/openai/linear_walkthrough.md",
        "llm_docs/personas_stories_openai.md": "softr/20251116_003000/docs/openai/personas_stories.md",
        "llm_docs/prd_document_openai.md": "softr/20251116_003000/docs/openai/prd_document.md",
        "llm_docs/linear_walkthrough_complete.md": "softr/20251116_003000/docs/unknown/linear_walkthrough.md",
        "llm_docs_enriched/linear_walkthrough_enriched.md": "softr/20251116_010000/docs/gemini_vision/linear_walkthrough.md",
        "llm_docs_enriched/personas_stories_enriched.md": "softr/20251116_010000/docs/gemini_vision/personas_stories.md",
        "llm_docs_enriched/prd_document_enriched.md": "softr/20251116_010000/docs/gemini_vision/prd_document.md",
    }
    
    # Collect all files from out/
    out_files = {}
    for file_path in out_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = str(file_path.relative_to(out_dir))
            out_files[rel_path] = {
                "path": file_path,
                "size": file_path.stat().st_size,
                "hash": file_hash(file_path)
            }
    
    # Collect all files from output/
    output_files = {}
    for file_path in output_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = str(file_path.relative_to(output_dir))
            output_files[rel_path] = {
                "path": file_path,
                "size": file_path.stat().st_size,
                "hash": file_hash(file_path),
                "base_name": file_path.name
            }
    
    # Create mapping
    mapped_count = 0
    unmapped_count = 0
    
    for out_rel, out_info in sorted(out_files.items()):
        out_name = Path(out_rel).name
        mapped = False
        
        # Check renamed mappings first
        if out_rel in renamed_mappings:
            output_rel = renamed_mappings[out_rel]
            output_path = output_dir / output_rel
            if output_path.exists():
                output_info = output_files[output_rel]
                if out_info["hash"] == output_info["hash"]:
                    mapping["files"].append({
                        "out_path": out_rel,
                        "output_path": output_rel,
                        "status": "mapped_renamed",
                        "size_match": out_info["size"] == output_info["size"],
                        "hash_match": True
                    })
                    mapped = True
                    mapped_count += 1
        
        # Try to find by filename
        if not mapped:
            for output_rel, output_info in output_files.items():
                if output_info["base_name"] == out_name:
                    if out_info["size"] == output_info["size"]:
                        if out_info["hash"] == output_info["hash"]:
                            mapping["files"].append({
                                "out_path": out_rel,
                                "output_path": output_rel,
                                "status": "mapped_exact",
                                "size_match": True,
                                "hash_match": True
                            })
                            mapped = True
                            mapped_count += 1
                            break
        
        if not mapped:
            mapping["files"].append({
                "out_path": out_rel,
                "output_path": None,
                "status": "unmapped",
                "size_match": False,
                "hash_match": False
            })
            unmapped_count += 1
    
    mapping["summary"] = {
        "total_files": len(out_files),
        "mapped": mapped_count,
        "unmapped": unmapped_count,
        "mapped_percentage": round(mapped_count / len(out_files) * 100, 1) if out_files else 0
    }
    
    # Save mapping
    mapping_path = Path("output/FILE_MAPPING.json")
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)
    
    print("=" * 80)
    print("FILE MAPPING CREATED")
    print("=" * 80)
    print(f"\nTotal files in out/: {mapping['summary']['total_files']}")
    print(f"Files mapped: {mapping['summary']['mapped']}")
    print(f"Files unmapped: {mapping['summary']['unmapped']}")
    print(f"Mapping saved to: {mapping_path}")
    
    if unmapped_count > 0:
        print(f"\n⚠ Unmapped files:")
        for item in mapping["files"]:
            if item["status"] == "unmapped":
                print(f"  - {item['out_path']}")
    
    return mapping


if __name__ == "__main__":
    create_mapping()

