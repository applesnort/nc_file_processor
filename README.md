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

### Prerequisites
- Python 3.8 or higher
- Windows (or macOS/Linux for development)

### Setup

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

3. The executable will be in the `dist` folder - just give `NCFileProcessor.exe` to your cousin!

**Note:** The .exe file will be large (~50-100MB) because it includes Python and all dependencies. This is normal for standalone executables.

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

## Testing on Mac

Yes! You can test and develop this on your Mac. CustomTkinter works on macOS, Linux, and Windows. Just install the dependencies and run:

```bash
pip install -r requirements.txt
python nc_file_processor.py
```

The drag-and-drop will work on Mac too! However, the final .exe build needs to be done on Windows (or using Wine/Cross-compilation tools).

## Pushing to GitHub

To push this to GitHub:

1. **Create a new repository on GitHub** (github.com/new)
   - **⚠️ IMPORTANT: Select "Public" (not Private)!**
   - Don't initialize with README (we already have one)
2. Run the setup script (or manually):
```bash
chmod +x setup_github.sh
./setup_github.sh
```

3. Add your GitHub remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

Or if you prefer to do it manually:
```bash
git init
git add .
git commit -m "Initial commit: NC File Processor"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

**To verify it's public:** After pushing, check your repository on GitHub. If it's public, you'll see a "Public" badge next to the repository name. If it's private, you can change it in Settings → General → Danger Zone → Change repository visibility.
