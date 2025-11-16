#!/usr/bin/env python3
"""
Verify that all files from out/ have been properly mapped to output/.
"""

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


def verify_mapping():
    """Verify all out/ files are mapped to output/."""
    out_dir = Path("out")
    output_dir = Path("output")
    
    if not out_dir.exists():
        print("No 'out' directory found")
        return
    
    # Collect all files from out/
    out_files = {}
    for file_path in out_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = file_path.relative_to(out_dir)
            out_files[str(rel_path)] = {
                "path": file_path,
                "size": file_path.stat().st_size,
                "hash": file_hash(file_path)
            }
    
    # Collect all files from output/
    output_files = {}
    for file_path in output_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            rel_path = file_path.relative_to(output_dir)
            # Extract base filename (without run structure)
            parts = rel_path.parts
            if len(parts) >= 3:  # video/timestamp/filename
                base_name = parts[-1]
                output_files[str(rel_path)] = {
                    "path": file_path,
                    "size": file_path.stat().st_size,
                    "hash": file_hash(file_path),
                    "base_name": base_name
                }
    
    print(f"Found {len(out_files)} files in out/")
    print(f"Found {len(output_files)} files in output/")
    print()
    
    # Create mapping
    mapping = defaultdict(list)
    unmapped = []
    
    for out_rel, out_info in out_files.items():
        out_name = Path(out_rel).name
        found = False
        
        # Try to find matching file in output/
        for output_rel, output_info in output_files.items():
            if output_info["base_name"] == out_name:
                # Verify it's the same file
                if out_info["size"] == output_info["size"]:
                    if out_info["hash"] == output_info["hash"]:
                        mapping[out_rel].append({
                            "output_path": output_rel,
                            "match": "exact"
                        })
                        found = True
                    else:
                        mapping[out_rel].append({
                            "output_path": output_rel,
                            "match": "size_only"
                        })
                        found = True
        
        if not found:
            unmapped.append(out_rel)
    
    # Print results
    print("=" * 80)
    print("FILE MAPPING VERIFICATION")
    print("=" * 80)
    print()
    
    if mapping:
        print(f"✓ Mapped files ({len(mapping)}):")
        for out_path, matches in sorted(mapping.items()):
            print(f"\n  {out_path}")
            for match in matches:
                status = "✓" if match["match"] == "exact" else "⚠"
                print(f"    {status} -> {match['output_path']} ({match['match']})")
    
    if unmapped:
        print(f"\n⚠ Unmapped files ({len(unmapped)}):")
        for path in sorted(unmapped):
            print(f"    - {path}")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files in out/: {len(out_files)}")
    print(f"Files mapped: {len(mapping)}")
    print(f"Files unmapped: {len(unmapped)}")
    
    exact_matches = sum(1 for matches in mapping.values() 
                       for m in matches if m["match"] == "exact")
    print(f"Exact matches (size + hash): {exact_matches}")
    
    if unmapped:
        print(f"\n⚠ WARNING: {len(unmapped)} files were not mapped!")
        return False
    else:
        print("\n✓ All files successfully mapped!")
        return True


if __name__ == "__main__":
    success = verify_mapping()
    exit(0 if success else 1)

