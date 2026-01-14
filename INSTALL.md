# Installation Instructions

## For Your Cousin (End User - Windows)

### Option 1: Use the Pre-built .exe (Easiest!)

1. Download `NCFileProcessor.exe` from the releases
2. Double-click the .exe file - that's it! No installation needed.
3. Drag & drop your NC file onto the window, or click "Select NC File"
4. Click "Process File"
5. Done! Your processed file will be saved in the same folder as the original

## For Developers

### Mac/Linux Development Setup

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python nc_file_processor.py
```

**Note:** The app works on Mac for development/testing, but the .exe build is Windows-only.

### Building Windows .exe

1. On Windows, install Python and dependencies:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

2. Run the build script:
```bash
build_exe.bat
```

Or manually:
```bash
pyinstaller --onefile --windowed --name "NCFileProcessor" --hidden-import=tkinterdnd2 --hidden-import=customtkinter nc_file_processor.py
```

3. The .exe will be in the `dist` folder
