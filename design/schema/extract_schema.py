#!/usr/bin/env python3
"""
Extract complete schema for all Airtable bases and categorize them as active vs legacy/test.
This script only fetches schema/metadata, not actual data.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    class tqdm:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def update(self, n=1):
            pass
        def set_description(self, desc=""):
            pass
        def write(self, msg):
            print(msg)

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env parsing if dotenv not available
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if "#" in line:
                    line = line.split("#")[0]
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_URL = "https://api.airtable.com/v0"
META_URL = "https://api.airtable.com/v0/meta"

def log_info(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] ℹ️  {msg}")

def log_success(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] ✅ {msg}")

def log_error(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] ❌ {msg}")

def make_request(url, silent=False, retries=2):
    """Make API request using urllib with retry logic."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:  # Increased timeout
                return response.getcode(), json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            try:
                error_body = json.loads(e.read().decode())
                return e.code, error_body
            except:
                if attempt < retries:
                    continue
                return e.code, {"error": str(e)}
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                continue
            return None, {"error": f"Timeout or connection error: {str(e)}"}
        except Exception as e:
            if attempt < retries:
                continue
            return None, {"error": str(e)}
    
    return None, {"error": "Max retries exceeded"}

def analyze_base_activity(base_id, base_name):
    """Analyze base activity by checking recent record creation/modification."""
    # Get a sample of records to check activity
    # First, get tables
    status, schema = make_request(f"{META_URL}/bases/{base_id}/tables", silent=True)
    if status != 200:
        return None
    
    tables = schema.get("tables", [])
    if not tables:
        return {
            "total_tables": 0,
            "total_records": 0,
            "recent_activity": False,
            "last_activity_date": None
        }
    
    # Check a few tables for recent activity
    total_records = 0
    recent_records = 0
    latest_date = None
    days_back = 90  # Consider activity in last 90 days as "recent"
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    # Sample up to 5 tables to check activity
    sample_tables = tables[:5]
    for table in sample_tables:
        table_id = table.get("id")
        # Get a small sample of records (10) to check dates
        status, records_data = make_request(
            f"{BASE_URL}/{base_id}/{table_id}?maxRecords=10&pageSize=10",
            silent=True
        )
        
        if status == 200:
            records = records_data.get("records", [])
            total_records += len(records)
            
            for record in records:
                # Check createdTime
                if "createdTime" in record:
                    created_str = record["createdTime"]
                    try:
                        created_date = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                        if latest_date is None or created_date > latest_date:
                            latest_date = created_date
                        if created_date > cutoff_date:
                            recent_records += 1
                    except:
                        pass
                
                # Check lastModifiedTime
                if "lastModifiedTime" in record:
                    modified_str = record["lastModifiedTime"]
                    try:
                        modified_date = datetime.fromisoformat(modified_str.replace("Z", "+00:00"))
                        if latest_date is None or modified_date > latest_date:
                            latest_date = modified_date
                        if modified_date > cutoff_date:
                            recent_records += 1
                    except:
                        pass
    
    return {
        "total_tables": len(tables),
        "total_records_sampled": total_records,
        "recent_activity": recent_records > 0,
        "recent_records": recent_records,
        "last_activity_date": latest_date.isoformat() if latest_date else None
    }

def classify_base(base_name, activity_data):
    """Classify a base as active, legacy, or test."""
    base_lower = base_name.lower()
    
    # Test bases - explicit test keywords
    test_keywords = ["test", "testing", "dev", "development", "staging", "sandbox", "demo", "[training]", "[testing area]"]
    if any(keyword in base_lower for keyword in test_keywords):
        return "test"
    
    # Legacy bases - explicit legacy keywords
    legacy_keywords = ["old", "archive", "backup", "deprecated", "copy", "scratch"]
    if any(keyword in base_lower for keyword in legacy_keywords):
        return "legacy"
    
    # Check for date patterns that suggest dated snapshots
    import re
    # Pattern: "Name (Month DD, YYYY)" or "Name MM/DD/YY" suggests a dated snapshot
    date_pattern = r'\([A-Za-z]+\s+\d{1,2},\s+\d{4}\)|\(\d{1,2}/\d{1,2}/\d{2,4}\)'
    has_date_pattern = bool(re.search(date_pattern, base_name))
    
    # Core infrastructure bases (no dates, likely main bases)
    core_bases = ["rrid reviewer selection process", "rrid_app_user", "rapid reviews"]
    is_core = any(core in base_lower for core in core_bases) and not has_date_pattern
    
    # Check activity
    if activity_data:
        total_records = activity_data.get("total_records_sampled", 0)
        recent_activity = activity_data.get("recent_activity", False)
        total_tables = activity_data.get("total_tables", 0)
        
        # Core infrastructure bases are active if they have substantial structure
        if is_core and total_tables > 5:
            return "active"
        
        # Bases with recent activity are active
        if recent_activity:
            return "active"
        
        # Dated bases without recent activity are legacy
        if has_date_pattern and not recent_activity:
            return "legacy"
        
        # Bases with substantial records but no dates might be active infrastructure
        if total_records > 20 and total_tables > 3 and not has_date_pattern:
            return "active"
        
        # Bases with no records are likely test
        if total_records == 0:
            return "test"
        
        # Default for bases with some records but no clear pattern
        if total_records > 0:
            return "legacy"  # Has data but no recent activity
    
    # Default: if it's a core base name without dates, assume active
    if is_core:
        return "active"
    
    # Default to legacy if we can't determine
    return "legacy"

def extract_complete_schema():
    """Extract complete schema for all bases."""
    if not API_KEY:
        log_error("AIRTABLE_API_KEY not found")
        sys.exit(1)
    
    log_info("Starting schema extraction...")
    log_info("Mode: Schema only (no data)")
    
    # Get user info
    log_info("Fetching user information...")
    status, user_info = make_request(f"{META_URL}/whoami", silent=True)
    if status != 200:
        log_error("Failed to authenticate")
        sys.exit(1)
    log_success(f"Authenticated as: {user_info.get('email', 'Unknown')}")
    
    # Get all bases
    log_info("Fetching list of bases...")
    status, bases_data = make_request(f"{META_URL}/bases", silent=True)
    if status != 200:
        log_error("Failed to retrieve bases")
        sys.exit(1)
    
    bases = bases_data.get("bases", [])
    log_success(f"Found {len(bases)} base(s)")
    
    # Extract schema for each base
    complete_schema = {
        "extracted_at": datetime.now().isoformat(),
        "user": user_info,
        "bases": []
    }
    
    log_info("Extracting schemas and analyzing activity...")
    
    with tqdm(total=len(bases), desc="Processing bases", unit="base") as pbar:
        for base in bases:
            base_id = base.get("id")
            base_name = base.get("name", "Unnamed")
            permission_level = base.get("permissionLevel", "Unknown")
            
            pbar.set_description(f"Base: {base_name[:25]}")
            
            # Get schema
            status, schema_data = make_request(f"{META_URL}/bases/{base_id}/tables", silent=True)
            if status != 200:
                log_error(f"{base_name}: Failed to get schema (Status {status})")
                pbar.update(1)
                continue
            
            # Analyze activity
            activity = analyze_base_activity(base_id, base_name)
            classification = classify_base(base_name, activity)
            
            base_schema = {
                "base_id": base_id,
                "base_name": base_name,
                "permission_level": permission_level,
                "classification": classification,
                "activity": activity,
                "url": f"https://airtable.com/{base_id}",
                "tables": []
            }
            
            # Process tables
            tables = schema_data.get("tables", [])
            for table in tables:
                table_schema = {
                    "table_id": table.get("id"),
                    "table_name": table.get("name"),
                    "primary_field_id": table.get("primaryFieldId"),
                    "fields": []
                }
                
                # Process fields
                for field in table.get("fields", []):
                    field_schema = {
                        "field_id": field.get("id"),
                        "field_name": field.get("name"),
                        "field_type": field.get("type"),
                        "options": field.get("options", {})
                    }
                    table_schema["fields"].append(field_schema)
                
                base_schema["tables"].append(table_schema)
            
            complete_schema["bases"].append(base_schema)
            pbar.update(1)
    
    # Categorize bases
    categorized = {
        "active": [],
        "legacy": [],
        "test": []
    }
    
    for base in complete_schema["bases"]:
        cat = base["classification"]
        categorized[cat].append(base)
    
    # Generate summary
    log_success("Schema extraction complete!")
    log_info(f"Total bases: {len(complete_schema['bases'])}")
    log_info(f"  Active: {len(categorized['active'])}")
    log_info(f"  Legacy: {len(categorized['legacy'])}")
    log_info(f"  Test: {len(categorized['test'])}")
    
    # Save complete schema
    output_file = Path("airtable_complete_schema.json")
    with open(output_file, 'w') as f:
        json.dump(complete_schema, f, indent=2)
    log_success(f"Complete schema saved to: {output_file}")
    
    # Save categorized schema
    categorized_file = Path("airtable_schema_categorized.json")
    with open(categorized_file, 'w') as f:
        json.dump(categorized, f, indent=2)
    log_success(f"Categorized schema saved to: {categorized_file}")
    
    # Generate markdown report
    md_file = Path("airtable_schema_report.md")
    generate_markdown_report(complete_schema, categorized, md_file)
    log_success(f"Markdown report saved to: {md_file}")
    
    return complete_schema, categorized

def generate_markdown_report(complete_schema, categorized, output_file):
    """Generate a markdown report of the schema."""
    with open(output_file, 'w') as f:
        f.write("# Airtable Complete Schema Report\n\n")
        f.write(f"**Extracted:** {complete_schema['extracted_at']}\n")
        f.write(f"**User:** {complete_schema['user'].get('email', 'Unknown')}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Bases:** {len(complete_schema['bases'])}\n")
        f.write(f"- **Active Bases:** {len(categorized['active'])}\n")
        f.write(f"- **Legacy Bases:** {len(categorized['legacy'])}\n")
        f.write(f"- **Test Bases:** {len(categorized['test'])}\n\n")
        
        # Active bases
        f.write("## Active Bases\n\n")
        for base in categorized['active']:
            f.write(f"### {base['base_name']}\n\n")
            f.write(f"- **ID:** `{base['base_id']}`\n")
            f.write(f"- **URL:** {base['url']}\n")
            f.write(f"- **Tables:** {len(base['tables'])}\n")
            if base['activity']:
                f.write(f"- **Recent Activity:** {'Yes' if base['activity'].get('recent_activity') else 'No'}\n")
            f.write(f"\n**Tables:**\n\n")
            for table in base['tables']:
                f.write(f"- **{table['table_name']}** ({len(table['fields'])} fields)\n")
            f.write("\n")
        
        # Legacy bases
        f.write("## Legacy Bases\n\n")
        for base in categorized['legacy']:
            f.write(f"### {base['base_name']}\n\n")
            f.write(f"- **ID:** `{base['base_id']}`\n")
            f.write(f"- **URL:** {base['url']}\n")
            f.write(f"- **Tables:** {len(base['tables'])}\n")
            f.write(f"- **Reason:** Dated or no recent activity\n\n")
        
        # Test bases
        f.write("## Test/Development Bases\n\n")
        for base in categorized['test']:
            f.write(f"### {base['base_name']}\n\n")
            f.write(f"- **ID:** `{base['base_id']}`\n")
            f.write(f"- **URL:** {base['url']}\n")
            f.write(f"- **Tables:** {len(base['tables'])}\n\n")

if __name__ == "__main__":
    try:
        extract_complete_schema()
    except KeyboardInterrupt:
        log_error("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

