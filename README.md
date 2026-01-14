# NC File Processor

A simple Windows GUI application for processing NC (Numerical Control) files. This tool automatically adds `G0` commands to lines with negative X values when the difference from the previous positive X value is 0.2 or greater.

## Features

- **Drag & Drop Support** - Simply drag your NC file onto the window
- **Simple, modern GUI** built with CustomTkinter
- **Non-destructive processing** - Creates new output file (original unchanged)
- **Automatic G0 prefix insertion** based on X-value differences
- **Easy file selection** - Click button or drag & drop
- **Processing log** - See exactly what changes were made
- **Open output folder** - Quick access to processed files
- **Standalone .exe** - No Python installation needed for end users

## Algorithm

The processor follows this logic:
1. Reads the NC file line by line
2. For each line with a negative X value (e.g., `-X1.915`)
3. Checks if the previous line had a positive X value
4. If the difference between the positive and absolute negative values is ≥ 0.2
5. Prepends `G0` to the line (if not already present)

## Installation

### For End Users (Download Pre-built .exe)

1. Go to [Releases](https://github.com/applesnort/nc_file_processor/releases)
2. Download `NCFileProcessor.exe` from the latest release
3. Double-click to run - no installation needed!

### For Developers

#### Prerequisites
- Python 3.8 or higher
- Windows (or macOS/Linux for development)

#### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python nc_file_processor.py
```

2. Click "Select NC File" to choose your input file
3. Click "Process File" to generate the modified output
4. The output file will be saved in the same directory as the input file with `_processed` added to the filename

## Building Windows Executable

To create a standalone Windows .exe file (for your cousin - no Python needed!):

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. On Windows, double-click `build_exe.bat` OR run:
```bash
pyinstaller --onefile --windowed --name "NCFileProcessor" --hidden-import=tkinterdnd2 --hidden-import=customtkinter nc_file_processor.py
```

3. The executable will be in the `dist` folder

**Note:** The .exe file will be large (~50-100MB) because it includes Python and all dependencies. This is normal for standalone executables.

## Creating GitHub Releases

This repository uses GitHub Actions to automatically build and create releases. To create a new release:

1. Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. GitHub Actions will automatically:
   - Build the Windows .exe on a Windows runner
   - Create a GitHub release
   - Attach the .exe file to the release

Alternatively, you can manually trigger the workflow from the GitHub Actions tab.

The release will appear at: https://github.com/applesnort/nc_file_processor/releases

## Example

**Input file:**
```
X1.915
-X1.715
X2.0
-X1.5
```

**Output file:**
```
X1.915
G0 -X1.715
X2.0
G0 -X1.5
```

(The second and fourth lines get `G0` prefix because the differences are ≥ 0.2)
