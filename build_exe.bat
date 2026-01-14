@echo off
echo Building NC File Processor executable...
echo.
echo This will create a standalone .exe file that your cousin can double-click to run.
echo No Python installation needed!
echo.
pause

pyinstaller --onefile --windowed --name "NCFileProcessor" --add-data "requirements.txt;." --hidden-import=tkinterdnd2 --hidden-import=customtkinter --collect-all tkinterdnd2 nc_file_processor.py

echo.
echo Build complete! Check the 'dist' folder for NCFileProcessor.exe
echo.
echo You can now give this .exe file to your cousin - no installation needed!
pause
