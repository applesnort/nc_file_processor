"""
NC File Processor - G-code modification tool
Processes NC files to add G0 commands based on X-value differences
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import re
import os
import sys
import subprocess
from pathlib import Path

# Try to import tkinterdnd2 for drag-and-drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Note: tkinterdnd2 not installed. Drag-and-drop disabled. Install with: pip install tkinterdnd2")

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NCFileProcessor(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Enable drag-and-drop on the root window if available
        if DND_AVAILABLE:
            # Make the root window a drop target
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.on_drop)
        
        self.title("NC File Processor")
        self.geometry("700x650")
        self.input_file_path = None
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="NC File G-Code Processor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        # Instructions
        self.instructions = ctk.CTkLabel(
            self.main_frame,
            text="Drag & drop an NC file here, or click 'Select File'\nLines with negative X values will be prefixed with G0\nif the difference from the previous positive X value is ≥ 0.2",
            font=ctk.CTkFont(size=11),
            justify="center"
        )
        self.instructions.pack(pady=(0, 20))
        
        # Drag and drop zone
        self.drop_zone = ctk.CTkFrame(
            self.main_frame,
            border_width=2,
            border_color="gray",
            corner_radius=10
        )
        self.drop_zone.pack(fill="x", pady=10, padx=10)
        
        self.drop_label = ctk.CTkLabel(
            self.drop_zone,
            text="📁 Drag & Drop NC File Here\n(or click Select File below)",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="center"
        )
        self.drop_label.pack(pady=30)
        
        # Enable drag and drop on drop zone if available
        if DND_AVAILABLE:
            # Get the underlying tkinter widget for drag-and-drop
            drop_zone_tk = self.drop_zone._canvas  # CustomTkinter uses a canvas internally
            drop_zone_tk.drop_target_register(DND_FILES)
            drop_zone_tk.dnd_bind('<<Drop>>', self.on_drop)
        
        # File selection frame
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.pack(fill="x", pady=10)
        
        self.file_label = ctk.CTkLabel(
            self.file_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.file_label.pack(fill="x", padx=20, pady=15)
        
        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", pady=10)
        
        self.select_button = ctk.CTkButton(
            self.button_frame,
            text="📂 Select NC File",
            command=self.select_file,
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.select_button.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        self.process_button = ctk.CTkButton(
            self.button_frame,
            text="⚙️ Process File",
            command=self.process_file,
            font=ctk.CTkFont(size=14),
            height=40,
            state="disabled"
        )
        self.process_button.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        self.open_folder_button = ctk.CTkButton(
            self.button_frame,
            text="📁 Open Output Folder",
            command=self.open_output_folder,
            font=ctk.CTkFont(size=12),
            height=40,
            state="disabled",
            fg_color="gray",
            hover_color="darkgray"
        )
        self.open_folder_button.pack(side="left", padx=5, pady=10, fill="x", expand=False)
        
        self.last_output_path = None
        
        # Status text area
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Status: Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)
        
        # Log textbox
        self.log_textbox = ctk.CTkTextbox(
            self.main_frame,
            height=150,
            font=ctk.CTkFont(size=11)
        )
        self.log_textbox.pack(fill="both", expand=True, pady=10)
        self.log_textbox.insert("1.0", "Ready to process NC files...\n")
        self.log_textbox.configure(state="disabled")
    
    def log_message(self, message):
        """Add a message to the log textbox"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
    
    def on_drop(self, event):
        """Handle file drop event"""
        try:
            # Get the dropped file path
            files = self.tk.splitlist(event.data)
            if files:
                file_path = files[0].strip('{}')  # Remove curly braces Windows adds
                # Handle Windows paths with curly braces
                file_path = file_path.strip('{}')
                if os.path.isfile(file_path):
                    self.load_file(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error handling dropped file: {str(e)}")
    
    def load_file(self, file_path):
        """Load a file and update UI"""
        # Validate it's an NC file
        if not file_path.lower().endswith('.nc'):
            result = messagebox.askyesno(
                "Not an NC file",
                f"The file '{os.path.basename(file_path)}' doesn't have a .nc extension.\n\n"
                "Do you want to process it anyway?"
            )
            if not result:
                return
        
        self.input_file_path = file_path
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_mb = file_size / (1024 * 1024)
        
        self.file_label.configure(text=f"Selected: {filename} ({size_mb:.2f} MB)")
        self.drop_label.configure(text=f"✓ {filename}\nReady to process")
        self.process_button.configure(state="normal")
        self.status_label.configure(text="Status: File selected - Ready to process")
        self.log_message(f"File loaded: {filename} ({size_mb:.2f} MB)")
    
    def select_file(self):
        """Open file dialog to select NC file"""
        file_path = filedialog.askopenfilename(
            title="Select NC File",
            filetypes=[("NC Files", "*.nc"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if self.last_output_path:
            folder_path = os.path.dirname(self.last_output_path)
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", folder_path])
                else:
                    subprocess.run(["xdg-open", folder_path])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {str(e)}")
    
    def extract_x_value(self, line):
        """
        Extract X value from a line.
        Returns the X value as float, or None if not found.
        Handles both positive (X1.915) and negative (-X1.915) formats.
        """
        # Pattern to match X followed by optional minus sign and number
        # Matches: X1.915, X-1.915, -X1.915, X 1.915, etc.
        pattern = r'[-\s]*X\s*([+-]?\d+\.?\d*)'
        match = re.search(pattern, line, re.IGNORECASE)
        
        if match:
            try:
                value = float(match.group(1))
                # Check if the line has a negative sign before X
                if re.search(r'-\s*X', line, re.IGNORECASE):
                    value = -abs(value)
                return value
            except ValueError:
                return None
        return None
    
    def process_file(self):
        """Process the NC file according to the algorithm"""
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        try:
            self.status_label.configure(text="Status: Processing...")
            self.log_message(f"\nProcessing file: {os.path.basename(self.input_file_path)}")
            
            # Read input file
            with open(self.input_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            processed_lines = []
            previous_x_value = None
            modifications_count = 0
            
            for i, line in enumerate(lines, 1):
                current_x = self.extract_x_value(line)
                
                # Check if current line has a negative X value
                if current_x is not None and current_x < 0:
                    # Check if previous line had a positive X value
                    if previous_x_value is not None and previous_x_value >= 0:
                        # Calculate difference
                        difference = previous_x_value - abs(current_x)
                        
                        # If difference is >= 0.2, prepend G0
                        if difference >= 0.2:
                            # Check if line doesn't already start with G0
                            stripped_line = line.lstrip()
                            if not stripped_line.upper().startswith('G0'):
                                line = "G0 " + line.lstrip()
                                modifications_count += 1
                                self.log_message(f"Line {i}: Added G0 prefix (diff: {difference:.3f})")
                
                # Update previous_x_value if current line has an X value
                if current_x is not None:
                    previous_x_value = current_x
                
                processed_lines.append(line)
            
            # Generate output filename
            input_path = Path(self.input_file_path)
            output_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(processed_lines)
            
            self.last_output_path = str(output_path)
            self.open_folder_button.configure(state="normal")
            
            self.status_label.configure(text=f"Status: Complete - {modifications_count} modifications made")
            self.log_message(f"\n✓ Processing complete!")
            self.log_message(f"✓ Output saved to: {output_path.name}")
            self.log_message(f"✓ Total modifications: {modifications_count}")
            self.drop_label.configure(text=f"✓ Processed!\n{output_path.name}")
            
            # Show success dialog with option to open folder
            result = messagebox.askyesno(
                "Success",
                f"File processed successfully!\n\n"
                f"Modifications: {modifications_count}\n"
                f"Output: {output_path.name}\n\n"
                f"Saved in: {input_path.parent}\n\n"
                f"Would you like to open the output folder?"
            )
            
            if result:
                self.open_output_folder()
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            self.log_message(f"\n✗ {error_msg}")
            self.status_label.configure(text="Status: Error occurred")
            messagebox.showerror("Error", error_msg)


if __name__ == "__main__":
    app = NCFileProcessor()
    app.mainloop()
