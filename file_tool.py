#!/usr/bin/env python3 
# This shebang makes this script executable on Unix-like systems (Linux, MacOS).

import os
import re
import argparse

import shutil
import sys
from pathlib import Path
from datetime import datetime

# Map extensions to folders
EXTENSION_MAP = {
	# Images
	'.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
	'.bmp': 'Images', '.svg': 'Images', '.ico': 'Images', '.webp': 'Images',
	# Documents
	'.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
	'.xls': 'Documents', '.xlsx': 'Documents', '.ppt': 'Documents',
	'.pptx': 'Documents', '.txt': 'Documents', '.rtf': 'Documents',
	'.odt': 'Documents', '.md': 'Documents',
	# Archives
	'.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
	'.tar': 'Archives', '.gz': 'Archives', '.bz2': 'Archives',
	# Audio
	'.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', '.aac': 'Audio',
	'.ogg': 'Audio', '.m4a': 'Audio',
	# Video
	'.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video', '.mov': 'Video',
	'.wmv': 'Video', '.flv': 'Video', '.webm': 'Video',
	# Code
	'.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code',
	'.cpp': 'Code', '.c': 'Code', '.java': 'Code', '.json': 'Code',
	'.xml': 'Code', '.sh': 'Code',
	# Executables
	'.exe': 'Programs', '.msi': 'Programs', '.deb': 'Programs',
	'.dmg': 'Programs', '.app': 'Programs',
}

# Unknown extension goes to other
DEFAULT_FOLDER = 'Other'

# This project is setup with dry_run mode. So some logics written for it.
# dry_run is shows simulated execution result but does not actually run the real operation
# also with option to copy or move
def sort_files(dir, dry_run=True, move=False):
	"""
	Shutil is used to copy/move
	Path is used to iterate source path, create destination path
	Datetime is used for distinct filename
	sys is used to separate content of stderr/stdin
	
	"""

	# Get folder's absolute path
	dir_path = Path(dir).resolve()

	# Validate folder's existence
	if not dir_path.is_dir():
		print(f"Error: {dir} is not a valid directory.", file=sys.stderr)
		return False

	files_moved = 0
	errors = 0

	for file in dir_path.iterdir():
		if not file.is_file():
			continue
		
		ext = file.suffix.lower()
		dest = EXTENSION_MAP.get(ext, DEFAULT_FOLDER)

		# destination folder parent path
		dest_dir = dir_path / dest
		
		# Create destination folder
		if not dry_run:
			dest_dir.mkdir(exist_ok=True) # if folder already exists, it won't crash

		# destination folder absolute path
		dest_path = dest_dir / file.name

		# Handle name conflicts
		if dest_path.exists():
			stem = file.stem
			# add timestamp for distinct filename
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			new_name = f"{stem}_{timestamp}{ext}"
			dest_path = dest_dir / new_name
		
		# Move file to destination folder absolute path
		try:
			if dry_run:
				action = "MOVE" if move else "COPY"
				print(f"[DRY RUN] {action}: {file.name} -> {dest_dir.name}/{dest_path.name}")
			else:
				if move:
					shutil.move(str(file), str(dest_path))
				else:
					shutil.copy2(str(file), str(dest_path))
				print(f"{'Moved' if move else 'Copied'}: {file.name} -> {dest_dir.name}/")
			files_moved += 1
		
		except (OSError, shutil.Error) as e:
			print(f"Error processing {file.name}: {e}", file=sys.stderr)
			errors += 1
		
	# Summary
	print(f"\nSummary: {files_moved} files processed, {errors} errors.")
	if dry_run:
		print("Dry run completed. No files were actually changed.")

	return errors == 0

sort_files(".")