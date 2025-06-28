import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.constants import *
import subprocess
import threading
import re
import os

class YTDLP_GUI:
    def __init__(self, master):
        self.master = master
        master.title("yt-dlp GUI (Refined)")
        master.geometry("800x680") # A little taller for the new option
        master.minsize(650, 550)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(3, weight=1) # The log frame row

        # --- Variables ---
        self.url_var = tk.StringVar()
        self.path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.format_var = tk.StringVar(value="video") # 'video', 'mp3', or 'wav'
        self.video_quality_var = tk.StringVar(value="Best")
        self.audio_quality_var = tk.StringVar(value="Best (VBR ~245k)")
        self.is_downloading = False

        # --- UI Sections ---
        self.create_input_frame()
        self.create_options_frame()
        self.create_action_frame()
        self.create_log_frame()
        
        # Set the initial state of the quality menus
        self.toggle_quality_controls()

    def create_input_frame(self):
        input_frame = ttk.Labelframe(self.master, text="Input", padding=(15, 10))
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Video URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, font=("Segoe UI", 10))
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Download Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.path_entry = ttk.Entry(input_frame, textvariable=self.path_var, state="readonly")
        self.path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_directory, bootstyle="secondary-outline")
        self.browse_button.grid(row=1, column=2, padx=(5, 0), pady=5)
        
    def create_options_frame(self):
        options_frame = ttk.Labelframe(self.master, text="Options", padding=(15, 10))
        options_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        options_frame.columnconfigure(1, weight=1)

        # Download Type Radio Buttons
        ttk.Label(options_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        format_group = ttk.Frame(options_frame)
        format_group.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Pass the same command to all radio buttons to update the UI
        ttk.Radiobutton(format_group, text="Video", variable=self.format_var, value="video", command=self.toggle_quality_controls).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(format_group, text="Audio (MP3)", variable=self.format_var, value="mp3", command=self.toggle_quality_controls).pack(side="left", padx=10)
        ttk.Radiobutton(format_group, text="Audio (WAV)", variable=self.format_var, value="wav", command=self.toggle_quality_controls).pack(side="left", padx=(10, 0))

        # Video Quality Dropdown
        ttk.Label(options_frame, text="Video Quality:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        video_q_options = ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"]
        self.video_quality_menu = ttk.Combobox(options_frame, textvariable=self.video_quality_var, values=video_q_options, state="readonly", bootstyle="info")
        self.video_quality_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Audio Quality Dropdown
        ttk.Label(options_frame, text="Audio Quality:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        audio_q_options = ["Best (VBR ~245k)", "High (VBR ~190k)", "Medium (VBR ~130k)", "Low (VBR ~100k)"]
        self.audio_quality_menu = ttk.Combobox(options_frame, textvariable=self.audio_quality_var, values=audio_q_options, state="disabled", bootstyle="info")
        self.audio_quality_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
    def create_action_frame(self):
        action_frame = ttk.Frame(self.master)
        action_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(action_frame, mode="determinate", bootstyle="success-striped")
        self.progress.grid(row=0, column=0, padx=0, pady=(0, 5), sticky="ew")

        self.download_button = ttk.Button(action_frame, text="Download", command=self.start_download, bootstyle="success")
        self.download_button.grid(row=1, column=0, pady=(5,0), ipady=5, sticky="ew")

    def create_log_frame(self):
        log_frame = ttk.Labelframe(self.master, text="Log & Status", padding=(15, 10))
        log_frame.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)

        self.status_var = tk.StringVar(value="Status: Idle")
        self.status_label = ttk.Label(log_frame, textvariable=self.status_var, font=("Segoe UI", 9, "italic"))
        self.status_label.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.log_text = ScrolledText(log_frame, wrap="word", height=10, autohide=True)
        self.log_text.grid(row=1, column=0, sticky="nsew")
        self.log_text.text.config(state="disabled")

    def toggle_quality_controls(self):
        """Enables and disables the quality menus based on format selection."""
        selected_format = self.format_var.get()
        if selected_format == "video":
            self.video_quality_menu.config(state="readonly")
            self.audio_quality_menu.config(state="disabled")
        elif selected_format == "mp3":
            self.video_quality_menu.config(state="disabled")
            self.audio_quality_menu.config(state="readonly")
        elif selected_format == "wav":
            # Quality setting doesn't apply to lossless WAV
            self.video_quality_menu.config(state="disabled")
            self.audio_quality_menu.config(state="disabled")
    
    def run_download_process(self):
        url = self.url_var.get()
        path = self.path_var.get()
        format_type = self.format_var.get()
        
        command = [
            'yt-dlp', '--progress', '--no-playlist',
            '--progress-template', 'download-specific:%(progress.percentage)s'
        ]

        if format_type == 'video':
            self.master.after(0, self.update_status, "Downloading video...")
            quality = self.video_quality_var.get()
            if quality != "Best":
                res = re.search(r'\d+', quality)
                if res:
                    format_string = f'bestvideo[height<={res.group(0)}]+bestaudio/best[height<={res.group(0)}]'
                    command += ['-f', format_string]

        elif format_type == 'mp3':
            self.master.after(0, self.update_status, "Downloading and converting to MP3...")
            command += ['-x', '--audio-format', 'mp3']
            
            # Map user-friendly quality to yt-dlp's 0-9 scale
            audio_q_map = {
                "Best (VBR ~245k)": "0",
                "High (VBR ~190k)": "2",
                "Medium (VBR ~130k)": "5",
                "Low (VBR ~100k)": "7"
            }
            yt_dlp_quality = audio_q_map.get(self.audio_quality_var.get(), "5") # Default to medium
            command += ['--audio-quality', yt_dlp_quality]

        elif format_type == 'wav':
            self.master.after(0, self.update_status, "Downloading and converting to WAV...")
            # For WAV, we just specify the format. No quality setting needed.
            command += ['-x', '--audio-format', 'wav']

        command += ['-P', path, url]

        # The rest of the function remains the same as the proven working version
        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, encoding='utf-8', errors='replace', startupinfo=startupinfo)

            is_determinate = False
            for line in iter(process.stdout.readline, ''):
                self.master.after(0, self.update_log, line)
                match = re.search(r'download-specific:(\d+\.?\d*)', line)
                if match:
                    if not is_determinate:
                        self.master.after(0, self.progress.stop)
                        self.master.after(0, self.progress.configure, {'mode': 'determinate', 'bootstyle': 'success-striped'})
                        is_determinate = True
                    percentage = float(match.group(1))
                    self.master.after(0, self.update_progress, percentage)

            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self.master.after(0, self.download_complete, True)
            else:
                self.master.after(0, self.download_complete, False, f"yt-dlp exited with error code {return_code}.")
        except FileNotFoundError:
            self.master.after(0, self.download_complete, False, "Error: 'yt-dlp' not found. Please ensure it is installed and in your system's PATH.")
        except Exception as e:
            self.master.after(0, self.download_complete, False, f"An unexpected error occurred: {e}")

    # --- Other methods are mostly unchanged ---

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.path_var.get())
        if directory:
            self.path_var.set(directory)

    def set_controls_state(self, state):
        """Enable or disable UI controls during download."""
        new_state = "normal" if state == "normal" else "disabled"
        self.url_entry.config(state=new_state)
        self.browse_button.config(state=new_state)
        
        # Disable all radio buttons and menus
        for widget in self.master.winfo_children()[1].winfo_children(): # Find widgets in "Options" frame
             if isinstance(widget, (ttk.Radiobutton, ttk.Combobox, ttk.Frame)):
                try: # Need to check if widget is a frame of radiobuttons
                    for child in widget.winfo_children():
                        child.config(state=new_state)
                except:
                    widget.config(state=new_state)
        
        # If enabling controls, re-evaluate which ones should be active
        if new_state == "normal":
            self.toggle_quality_controls()

    def start_download(self):
        if self.is_downloading:
            return
        url = self.url_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.", parent=self.master)
            return

        self.is_downloading = True
        self.download_button.config(state="disabled", text="Downloading...")
        self.set_controls_state("disabled")
        self.status_var.set("Status: Preparing to download...")
        self.progress["value"] = 0
        self.progress.configure(mode='indeterminate', bootstyle='info-striped')
        self.progress.start()

        self.log_text.text.config(state="normal")
        self.log_text.text.delete(1.0, tk.END)
        self.log_text.text.config(state="disabled")

        threading.Thread(target=self.run_download_process, daemon=True).start()

    def update_progress(self, value):
        self.progress["value"] = value

    def update_status(self, text):
        self.status_var.set(f"Status: {text}")

    def update_log(self, text):
        self.log_text.text.config(state="normal")
        self.log_text.text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.text.config(state="disabled")

    def download_complete(self, success, message=None):
        self.is_downloading = False
        self.progress.stop()
        
        if success:
            self.status_var.set("Status: Download finished successfully!")
            self.progress["value"] = 100
            self.progress.configure(bootstyle='success')
            messagebox.showinfo("Success", "Download complete!", parent=self.master)
        else:
            self.status_var.set(f"Status: Download failed! Check log for details.")
            self.progress.configure(bootstyle='danger')
            messagebox.showerror("Error", f"Download failed!\n\n{message or 'Check the log for details.'}", parent=self.master)
        
        self.download_button.config(state="normal", text="Download")
        self.set_controls_state("normal")


if __name__ == "__main__":
    # Themes: superhero, darkly, cyborg, vapor
    root = ttk.Window(themename="superhero") 
    app = YTDLP_GUI(root)
    root.mainloop()