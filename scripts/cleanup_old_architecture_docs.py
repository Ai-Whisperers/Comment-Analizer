#!/usr/bin/env python3
"""
Architecture Documentation Cleanup Script
Purpose: Remove old duplicated graph system documentation to prevent AI confusion
Strategy: Keep useful_architecture_map.md as single source of truth
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

def get_project_root():
    """Get the project root directory"""
    script_dir = Path(__file__).parent
    return script_dir.parent

def log_action(action, path, reason=""):
    """Log cleanup actions"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {action}: {path} {reason}")

def identify_old_graph_files():
    """Identify old graph system files that need cleanup"""
    project_root = get_project_root()
    
    # Primary old graph system files (highest priority for removal)
    primary_old_files = [
        "docs/arquitectura/00_Master_Graph_Navigation.md",
        "docs/arquitectura/Hierarchical_Graph_System_Design.md", 
        "docs/arquitectura/Interactive_Graph_Explorer.md",
        "docs/arquitectura/Complete_Vertex_Inventory.md",
        "docs/arquitectura/Component_Dependencies.md"
    ]
    
    # Subgraph directories (complete removal)
    old_subgraph_dirs = [
        "docs/arquitectura/subgraphs/"
    ]
    
    # Files to archive (keep for reference but move out of main docs)
    archive_files = [
        "docs/arquitectura/AI_Pipeline_Architecture_Report.md",
        "docs/arquitectura/E2E_Codebase_Analysis_Report.md", 
        "docs/arquitectura/Pipeline_Flow_Diagram.md",
        "docs/arquitectura/Methodological_Framework.md"
    ]
    
    return primary_old_files, old_subgraph_dirs, archive_files

def create_backup_before_cleanup():
    """Create backup of docs before cleanup"""
    project_root = get_project_root()
    backup_dir = project_root / "docs-backup-before-cleanup"
    
    if backup_dir.exists():
        log_action("SKIP", "backup already exists", str(backup_dir))
        return backup_dir
        
    # Create backup
    shutil.copytree(project_root / "docs", backup_dir)
    log_action("BACKUP", str(backup_dir), "created")
    return backup_dir

def cleanup_old_graph_files(dry_run=True):
    """Remove old graph system files"""
    project_root = get_project_root()
    primary_files, subgraph_dirs, archive_files = identify_old_graph_files()
    
    removed_count = 0
    archived_count = 0
    
    print(f"\n🧹 ARCHITECTURE DOCUMENTATION CLEANUP")
    print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL CLEANUP'}")
    print(f"Project root: {project_root}")
    
    # 1. Remove primary old graph files
    print(f"\n📁 Removing primary old graph files:")
    for rel_path in primary_files:
        full_path = project_root / rel_path
        if full_path.exists():
            if not dry_run:
                full_path.unlink()
                log_action("REMOVED", rel_path)
            else:
                log_action("WOULD REMOVE", rel_path)
            removed_count += 1
        else:
            log_action("NOT FOUND", rel_path)
    
    # 2. Remove subgraph directories completely
    print(f"\n📂 Removing subgraph directories:")
    for rel_path in subgraph_dirs:
        full_path = project_root / rel_path
        if full_path.exists():
            if not dry_run:
                shutil.rmtree(full_path)
                log_action("REMOVED DIR", rel_path)
            else:
                log_action("WOULD REMOVE DIR", rel_path)
            removed_count += 1
        else:
            log_action("NOT FOUND DIR", rel_path)
    
    # 3. Archive useful reports (move to archive folder)
    archive_dir = project_root / "docs/archive"
    print(f"\n📦 Archiving useful reports to {archive_dir}:")
    
    if not dry_run and not archive_dir.exists():
        archive_dir.mkdir(parents=True)
        log_action("CREATED", str(archive_dir))
    
    for rel_path in archive_files:
        full_path = project_root / rel_path
        if full_path.exists():
            archive_path = archive_dir / Path(rel_path).name
            if not dry_run:
                shutil.move(str(full_path), str(archive_path))
                log_action("ARCHIVED", f"{rel_path} → {archive_path}")
            else:
                log_action("WOULD ARCHIVE", f"{rel_path} → {archive_path}")
            archived_count += 1
        else:
            log_action("NOT FOUND", rel_path)
    
    # 4. Verify new useful map exists
    useful_map = project_root / "local-reports/useful_architecture_map.md"
    if useful_map.exists():
        log_action("VERIFIED", "useful_architecture_map.md exists")
    else:
        log_action("ERROR", "useful_architecture_map.md NOT FOUND!", "❌")
        return False
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"Files removed: {removed_count}")
    print(f"Files archived: {archived_count}")
    print(f"New single source: local-reports/useful_architecture_map.md")
    
    return True

def calculate_size_reduction():
    """Calculate documentation size reduction"""
    project_root = get_project_root()
    
    # Old system size
    old_docs_size = 0
    if (project_root / "docs/arquitectura").exists():
        for root, dirs, files in os.walk(project_root / "docs/arquitectura"):
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    old_docs_size += file_path.stat().st_size
    
    # New system size
    useful_map = project_root / "local-reports/useful_architecture_map.md"
    new_size = useful_map.stat().st_size if useful_map.exists() else 0
    
    print(f"\n📊 SIZE ANALYSIS:")
    print(f"Old documentation: {old_docs_size:,} bytes ({old_docs_size/1024:.1f}KB)")
    print(f"New documentation: {new_size:,} bytes ({new_size/1024:.1f}KB)")
    if old_docs_size > 0:
        reduction_percent = ((old_docs_size - new_size) / old_docs_size) * 100
        print(f"Size reduction: {reduction_percent:.1f}% ({(old_docs_size-new_size)/1024:.1f}KB saved)")
        print(f"Token estimate reduction: ~{(old_docs_size-new_size)/4:.0f} tokens saved")

def main():
    """Main cleanup orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up old architecture documentation')
    parser.add_argument('--dry-run', action='store_true', default=True, 
                       help='Show what would be done without making changes')
    parser.add_argument('--execute', action='store_true', default=False,
                       help='Actually perform the cleanup')
    parser.add_argument('--backup', action='store_true', default=True,
                       help='Create backup before cleanup')
    
    args = parser.parse_args()
    
    # Override dry_run if --execute is specified
    dry_run = not args.execute
    
    print("🗑️ ARCHITECTURE DOCUMENTATION CLEANUP TOOL")
    print("=" * 50)
    
    # Show current state
    calculate_size_reduction()
    
    # Create backup if requested and not dry run
    if args.backup and not dry_run:
        backup_dir = create_backup_before_cleanup()
        print(f"✅ Backup created: {backup_dir}")
    
    # Perform cleanup
    success = cleanup_old_graph_files(dry_run=dry_run)
    
    if success:
        if dry_run:
            print(f"\n✅ DRY RUN COMPLETE - No files were modified")
            print(f"💡 Run with --execute to perform actual cleanup")
        else:
            print(f"\n✅ CLEANUP COMPLETE")
            calculate_size_reduction()
    else:
        print(f"\n❌ CLEANUP FAILED")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())