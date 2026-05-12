#!/usr/bin/env python3 
# This shebang makes this script executable on Unix-like systems (Linux, MacOS).

import os
import shutil
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime

# Extension mapping
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

for key,value in EXTENSION_MAP.items():
	print(f"{key}:{value}")