# Quick Start Guide

## For Your Cousin (Non-Technical User)

### The Easiest Way:
1. **Get the .exe file** - Once built, just double-click `NCFileProcessor.exe`
2. **Drag your NC file** onto the window (or click "Select NC File")
3. **Click "Process File"**
4. **Done!** Your processed file will be in the same folder with `_processed` added to the name

That's it! No installation, no setup, just double-click and go.

## For You (Developer)

### Test on Mac:
```bash
cd /Users/jorml/nc_file_processor
pip install -r requirements.txt
python nc_file_processor.py
```

**Yes, it works on Mac!** CustomTkinter is cross-platform. You can develop and test on your Mac, then build the .exe on Windows.

### Push to GitHub:

**Option 1: Use the script**
```bash
cd /Users/jorml/nc_file_processor
./setup_github.sh
# Then follow the instructions it prints
```

**Option 2: Manual**
```bash
cd /Users/jorml/nc_file_processor
git init
git add .
git commit -m "Initial commit: NC File Processor"
# Create repo on GitHub (make sure to select PUBLIC!), then:
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

**⚠️ Important:** When creating the repository on GitHub, make sure to select **"Public"** (not Private) so others can access it!

### Build Windows .exe (on Windows PC):
```bash
pip install pyinstaller
build_exe.bat
# Or manually:
pyinstaller --onefile --windowed --name "NCFileProcessor" --hidden-import=tkinterdnd2 --hidden-import=customtkinter nc_file_processor.py
```

The .exe will be in the `dist` folder - give that to your cousin!

## New Features Added

✅ **Drag & Drop** - Just drag files onto the window  
✅ **Visual feedback** - See file size, processing status  
✅ **Open output folder** - Quick access button  
✅ **Better error handling** - Clear messages if something goes wrong  
✅ **File validation** - Warns if file doesn't have .nc extension  
✅ **Processing log** - See exactly what changed  
✅ **Standalone .exe** - No Python needed for end users  

## Files Created

- `nc_file_processor.py` - Main application
- `requirements.txt` - Python dependencies
- `build_exe.bat` - Windows build script
- `setup_github.sh` - GitHub setup helper
- `README.md` - Full documentation
- `INSTALL.md` - Installation instructions
- `.gitignore` - Git ignore file
- `test_sample.nc` - Sample test file
