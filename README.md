### File Organizer & Bulk Renamer

A small, portable Python CLI tool to **organize files by extension** and **bulk rename files** in a directory. Supports dry-run previews, move vs copy behavior, regex and simple replacements, sequential numbering, and conflict-safe renaming.

---

#### Features
- **Organize files** into categorized folders (Images, Documents, Audio, Video, Code, Archives, Programs, Other).
- **Bulk rename** with prefix, suffix, replace, regex substitution, case conversion, and sequential numbering.
- **Dry-run mode** to preview changes without modifying files.
- **Move or copy** behavior for organizing.
- **Conflict handling**: appends timestamp to avoid overwriting.
- **Cross-platform**: uses `pathlib` and standard library only.

---

#### Installation
1. Ensure **Python 3.8+** is installed.
2. Save the script as `file_tool.py`.
3. Make it executable on Unix systems:
```bash
chmod +x file_tool.py
```

---

#### Usage
Run the script with one of two subcommands: `organize` or `rename`.

##### Organize
**Purpose**: Move or copy files into folders by extension.

**Basic command**
```bash
python file_tool.py organize /path/to/directory
```

**Move files instead of copying**
```bash
python file_tool.py organize /path/to/directory --move
```

**Preview changes without touching files**
```bash
python file_tool.py organize /path/to/directory --dry-run
```

##### Rename
**Purpose**: Bulk rename files with many transformation options.

**Basic command**
```bash
python file_tool.py rename /path/to/directory --prefix "vacation_"
```

**Replace text and change case**
```bash
python file_tool.py rename /path/to/directory --replace " " "_" --case lower --dry-run
```

**Regex substitution and sequential numbering**
```bash
python file_tool.py rename /path/to/directory --regex "IMG_(\d+)" "photo_\\1" --sequential --start 1
```

---

#### Command Options
| Option | Applies to | Description |
|---|---:|---|
| `--move` | organize | Move files instead of copying |
| `--dry-run` | organize, rename | Preview actions without changing files |
| `--prefix` | rename | Text to add at the beginning of filenames |
| `--suffix` | rename | Text to add before the extension |
| `--replace OLD NEW` | rename | Simple string replacement in filename |
| `--regex PATTERN REPL` | rename | `re.sub()` substitution on filename stem |
| `--case` | rename | `upper`, `lower`, or `title` case conversion |
| `--sequential` | rename | Replace filename with sequential numbers |
| `--start N` | rename | Starting number for sequential mode |
| `--filter EXT` | rename | Only process files with this extension |

---

#### Examples
- **Organize Downloads by copying**:
```bash
python file_tool.py organize ~/Downloads
```
- **Organize and move with preview**:
```bash
python file_tool.py organize ~/Downloads --move --dry-run
```
- **Add prefix to all files in a folder**:
```bash
python file_tool.py rename ~/Pictures --prefix "2026_"
```
- **Rename only .txt files sequentially starting at 1**:
```bash
python file_tool.py rename ~/notes --filter .txt --sequential --start 1 --dry-run
```