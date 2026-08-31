#!/usr/bin/env python3
"""Script to create a compressed ZIP file of the entire project."""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime


def create_project_archive(project_path=".", output_name=None):
    """Create a compressed ZIP file of the project.
    
    Args:
        project_path: Path to the project directory
        output_name: Name of the output ZIP file (default: gold-ai-advisor-YYYYMMDD.zip)
    """
    
    # Determine output filename
    if output_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"gold-ai-advisor-{timestamp}.zip"
    
    # Files and directories to exclude
    exclude_dirs = {
        '__pycache__',
        '.pytest_cache',
        '.tox',
        '.venv',
        'venv',
        'env',
        'node_modules',
        '.git',
        '.vscode',
        '.idea',
        'dist',
        'build',
        '*.egg-info',
        'logs',
        '__pycache__',
        '.DS_Store',
    }
    
    exclude_files = {
        '.env',
        '*.pyc',
        '*.pyo',
        '.DS_Store',
        'Thumbs.db',
        '*.log',
    }
    
    def should_exclude(path):
        """Check if a path should be excluded."""
        parts = Path(path).parts
        
        for part in parts:
            if part in exclude_dirs:
                return True
            for pattern in exclude_files:
                if pattern.startswith('*'):
                    if part.endswith(pattern[1:]):
                        return True
                elif part == pattern:
                    return True
        
        return False
    
    # Create ZIP file
    print(f"📦 Creating archive: {output_name}")
    print(f"📁 Source directory: {os.path.abspath(project_path)}")
    
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(project_path):
            # Filter directories
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip excluded files
                if should_exclude(file_path):
                    continue
                
                # Calculate archive name (relative path)
                arcname = os.path.relpath(file_path, os.path.dirname(project_path))
                
                # Add file to archive
                zipf.write(file_path, arcname=arcname)
                
                total_files += 1
                total_size += os.path.getsize(file_path)
                
                print(f"  ✓ Added: {arcname}")
    
    # Print summary
    archive_size = os.path.getsize(output_name)
    print(f"\n✅ Archive created successfully!")
    print(f"📊 Statistics:")
    print(f"   Files included: {total_files}")
    print(f"   Original size: {total_size / (1024*1024):.2f} MB")
    print(f"   Compressed size: {archive_size / (1024*1024):.2f} MB")
    print(f"   Compression ratio: {(1 - archive_size/total_size)*100:.1f}%")
    print(f"\n📍 Archive location: {os.path.abspath(output_name)}")
    
    return output_name


if __name__ == "__main__":
    import sys
    
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        create_project_archive(project_path, output_name)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
