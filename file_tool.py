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
def organize_files(dir, dry_run=True, move=False):
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

def bulk_renamer(dir, prefix='', suffix='', replace=None, case=None, regex=None, sequential=False, start_num=1, filter_ext=None, dry_run=False):
	"""
	Path is used to iterate source path, create destination path, and rename
	Datetime is used for distinct filename
	sys is used to separate content of stderr/stdin
	re is used for regex substitution
	
	string methods used replace, zfill
	list methods used sort
	"""

	# Source path
	dir_path = Path(dir).resolve() # absolute path
	if not dir_path.is_dir():
		print(f"Error: {dir} is not a valid directory.", file=sys.stderr)
		return False

	# filter by files
	files = [f for f in dir_path.iterdir() if f.is_file()]
	
	# filter by extension if exists
	if filter_ext:
		files = [f for f in files if f.suffix.lower() == filter_ext.lower()]

	# sort files by name
	files.sort(key=lambda x: x.name)

	renamed = 0
	errors = 0

	for i, file_path in enumerate(files, start=start_num):
		stem = file_path.stem
		ext = file_path.suffix

		new_stem = stem

		# Apply transformations in order:

		# replace
		if replace:
			# unpacking like destructuring in js
			old, new = replace
			new_stem = new_stem.replace(old, new)

		# regex
		if regex:
			pattern, repl = regex
			new_stem = re.sub(pattern, repl, new_stem)

		# prefix
		if prefix:
			new_stem = prefix + new_stem

		# suffix
		if suffix:
			new_stem = new_stem + suffix

		# case
		# strings are immutable, these methods return new string
		if case == 'upper':
			new_stem = new_stem.upper()
		elif case == 'lower':
			new_stem = new_stem.lower()
		elif case == 'title':
			new_stem = new_stem.title()

		# sequential
		if sequential:
			# eg: 001 ... 045
			last_num = len(files) + start_num - 1
			padding = len(str(last_num)) # count digit
			new_stem = str(i).zfill(padding) # string method to pad left side with zeros
		
		new_name = new_stem + ext
		new_path = dir_path / new_name

		# if the new name same as existing name, skip next renaming process
		if new_path == file_path:
			continue

		if new_path.exists():
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			new_name = f"{new_stem}_{timestamp}{ext}"
			new_path = dir_path / new_name
		
		try:
			if dry_run:
				print(f"[DRY RUN] Rename: {file_path.name} -> {new_name}")
			else:
				file_path.rename(new_path)
				print(f"Rename: {file_path.name} -> {new_name}")
			renamed += 1
		except OSError as e:
			print(f"Error renaming {file_path.name}: {e}", file=sys.stderr)
			errors += 1
		
	print(f"\nSummary: {renamed} files renamed, {errors} errors.")
	if dry_run:
		print("Dry run completed. No files were actually changed.")
	return errors == 0

def main():
	# All these keywords shown when executing --help
	parser = argparse.ArgumentParser(
		# Text shown at the top of the --help output.
		description="File Organizer & Bulk Renamer",
		# Format text - preserves line breaks and spaces
		formatter_class=argparse.RawDescriptionHelpFormatter,
		# Text shown at the bottom of the --help output.
		epilog="""
Examples:
# Organize files (copy)
python file_tool.py organize ~/Downloads

# Organize and move files (dry run)
python file_tool.py organize ~/Downloads --move --dry-run

# Add prefix to all files
python file_tool.py rename ~/Documents --prefix "vacation_"

# Replace spaces with underscores and convert to lowercase
python file_tool.py rename ~/Music --replace " " "_" --case lower

# Rename only .txt files sequentially
python file_tool.py rename ~/notes --filter .txt --sequential --start 1
"""
	)

	# Creates an object that will hold all subcommands added in args.command
	subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-commands')

	# Organize subcommand
	# Add subcommand 'organize'
	org_parser = subparsers.add_parser('organize', help='Organize files by extension')

	# Add arguments 'directory', 'move', and 'dry-run'
	org_parser.add_argument('directory', help='Directory to organize')

	# -- means optional
	org_parser.add_argument('--move', action='store_true', help='Move files instead of copying.')
	org_parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')

	# Rename subcommand
	# Define subcommand 'rename'
	rename_parser = subparsers.add_parser('rename', help='Bulk rename files')

	# Add arguments
	rename_parser.add_argument('directory', help='Directory containing files')

	rename_parser.add_argument('--prefix', default='', help='Text to add at beginning')
	rename_parser.add_argument('--suffix', default='', help='Text to add before extension')

	rename_parser.add_argument('--replace', nargs=2, metavar=('OLD','NEW'), help='Replace OLD with NEW in filename')
	rename_parser.add_argument('--regex', nargs=2, metavar=('PATTERN','REPL'), help='Regex substitution (re.sub())')

	rename_parser.add_argument('--case', choices=['upper', 'lower', 'title'], help='Change filename case')

	rename_parser.add_argument('--sequential', action='store_true', help='Rename files with sequential numbers')

	rename_parser.add_argument('--start', type=int, default=1, metavar='N', help='Starting number for sequential (default: 1)')

	rename_parser.add_argument('--filter', dest='filter_ext', metavar='EXT', help='Only process files with this extension (e.g., .txt)')

	rename_parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')

	# Parsing the Arguments
	args = parser.parse_args()

	if args.command == 'organize':
		# For option args, by default, argparse strips leading dashes -- and replaces dash with underscore _
		success = organize_files(args.directory, dry_run=args.dry_run,move=args.move)
	elif args.command == 'rename':
		# destructuring for multiple arguments
		replace_tuple = tuple(args.replace) if args.replace else None
		regex_tuple = tuple(args.regex) if args.regex else None

		success = bulk_renamer(
			args.directory,
			prefix=args.prefix,
			suffix=args.suffix,
			replace=replace_tuple,
			regex=regex_tuple,
			case=args.case,
			sequential=args.sequential,
			start_num=args.start,
			filter_ext=args.filter_ext,
			dry_run=args.dry_run
		)

	sys.exit(0 if success else 1)

if __name__ == '__main__':
	main()