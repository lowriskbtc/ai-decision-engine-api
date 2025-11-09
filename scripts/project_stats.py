"""
Project Statistics
Generate comprehensive project statistics
"""

import os
from pathlib import Path
from datetime import datetime
import json

def get_project_stats():
    """Get comprehensive project statistics"""
    project_root = Path(__file__).parent.parent
    
    stats = {
        "generated_at": datetime.now().isoformat(),
        "project_name": "AI Decision Engine API",
        "directories": {},
        "files": {
            "total": 0,
            "by_type": {},
            "by_directory": {}
        },
        "code": {
            "python_files": 0,
            "total_lines": 0,
            "api_endpoints": 0
        }
    }
    
    # Count files
    for root, dirs, files in os.walk(project_root):
        # Skip backup and cache directories
        if "BACKUP_" in root or "__pycache__" in root:
            continue
        
        rel_root = os.path.relpath(root, project_root)
        
        for file in files:
            if file.startswith("."):
                continue
            
            stats["files"]["total"] += 1
            
            # Count by type
            ext = os.path.splitext(file)[1] or "no_extension"
            stats["files"]["by_type"][ext] = stats["files"]["by_type"].get(ext, 0) + 1
            
            # Count by directory
            if rel_root not in stats["files"]["by_directory"]:
                stats["files"]["by_directory"][rel_root] = 0
            stats["files"]["by_directory"][rel_root] += 1
            
            # Count Python files and lines
            if file.endswith(".py"):
                stats["code"]["python_files"] += 1
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        lines = len(f.readlines())
                        stats["code"]["total_lines"] += lines
                except:
                    pass
    
    # Count API endpoints (approximate)
    api_main = project_root / "api" / "main.py"
    if api_main.exists():
        with open(api_main, "r", encoding="utf-8") as f:
            content = f.read()
            stats["code"]["api_endpoints"] = content.count("@app.")
    
    return stats

def print_stats(stats):
    """Print formatted statistics"""
    print("=" * 60)
    print("PROJECT STATISTICS")
    print("=" * 60)
    print()
    print(f"Project: {stats['project_name']}")
    print(f"Generated: {stats['generated_at']}")
    print()
    print("FILES:")
    print(f"  Total files: {stats['files']['total']}")
    print(f"  Python files: {stats['code']['python_files']}")
    print(f"  Total lines of code: {stats['code']['total_lines']:,}")
    print()
    print("API:")
    print(f"  Endpoints: {stats['code']['api_endpoints']}")
    print()
    print("FILE TYPES:")
    for ext, count in sorted(stats['files']['by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ext or 'no extension'}: {count}")

def main():
    """Generate and display statistics"""
    stats = get_project_stats()
    print_stats(stats)
    
    # Save to file
    with open("project_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Statistics saved to: project_stats.json")

if __name__ == "__main__":
    main()

