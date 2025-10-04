import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from core.encoder import VideoEncoder
from core.decoder import VideoDecoder


class MainWindow(tk.Tk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.title("YouTube Storage Tool")
        self.geometry("600x650")
        
        # Initialize encoders/decoders
        self.encoder = VideoEncoder(logger=self.log_message)
        self.decoder = VideoDecoder(logger=self.log_message)
        
        # Variables
        self.encode_filepath = tk.StringVar()
        self.decode_filepath = tk.StringVar()
        
        # Create widgets
        self.create_widgets()
    
    def log_message(self, message):
        """Insert a message into the status log text widget."""
        self.status_log.config(state=tk.NORMAL)
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.config(state=tk.DISABLED)
        self.status_log.see(tk.END)  # Auto-scroll to the bottom
        self.update_idletasks()
    
    def create_widgets(self):
        """Create and arrange all UI elements."""
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Encoding Section
        self.create_encoding_section(main_frame)
        
        # Decoding Section
        self.create_decoding_section(main_frame)
        
        # Status Log Section
        self.create_log_section(main_frame)
    
    def create_encoding_section(self, parent):
        """Create the encoding section UI."""
        encode_frame = tk.LabelFrame(parent, text=" 📁 Encode File to Video ", padx=10, pady=10)
        encode_frame.pack(fill=tk.X, expand=True, pady=(0, 10))
        
        tk.Label(encode_frame, text="File to Encode:").grid(row=0, column=0, sticky="w", pady=2)
        encode_entry = tk.Entry(encode_frame, textvariable=self.encode_filepath, state="readonly", width=50)
        encode_entry.grid(row=1, column=0, sticky="we")
        
        select_file_btn = tk.Button(encode_frame, text="Browse...", command=self.select_encode_file)
        select_file_btn.grid(row=1, column=1, padx=(5, 0))
        
        self.start_encode_btn = tk.Button(encode_frame, text="▶️ Start Encoding", command=self.start_encoding_thread)
        self.start_encode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")
    
    def create_decoding_section(self, parent):
        """Create the decoding section UI."""
        decode_frame = tk.LabelFrame(parent, text=" 🎥 Decode Video to File ", padx=10, pady=10)
        decode_frame.pack(fill=tk.X, expand=True, pady=10)
        
        tk.Label(decode_frame, text="Video to Decode:").grid(row=0, column=0, sticky="w", pady=2)
        decode_entry = tk.Entry(decode_frame, textvariable=self.decode_filepath, state="readonly", width=50)
        decode_entry.grid(row=1, column=0, sticky="we")
        
        select_video_btn = tk.Button(decode_frame, text="Browse...", command=self.select_decode_video)
        select_video_btn.grid(row=1, column=1, padx=(5, 0))
        
        self.start_decode_btn = tk.Button(decode_frame, text="◀️ Start Decoding", command=self.start_decoding_thread)
        self.start_decode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")
    
    def create_log_section(self, parent):
        """Create the status log section UI."""
        log_frame = tk.LabelFrame(parent, text=" 📊 Status Log ", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_log = scrolledtext.ScrolledText(log_frame, state="disabled", height=10, wrap=tk.WORD)
        self.status_log.pack(fill=tk.BOTH, expand=True)
    
    def select_encode_file(self):
        """Open file dialog to select a file for encoding."""
        filepath = filedialog.askopenfilename(title="Select a file to encode")
        if filepath:
            self.encode_filepath.set(filepath)
            self.log_message(f"Selected for encoding: {os.path.basename(filepath)}")
    
    def select_decode_video(self):
        """Open file dialog to select a video for decoding."""
        filepath = filedialog.askopenfilename(
            title="Select a video to decode",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*"))
        )
        if filepath:
            self.decode_filepath.set(filepath)
            self.log_message(f"Selected for decoding: {os.path.basename(filepath)}")
    
    def set_buttons_state(self, state):
        """Enable or disable the start buttons."""
        self.start_encode_btn.config(state=state)
        self.start_decode_btn.config(state=state)
    
    def start_encoding_thread(self):
        """Start encoding in a separate thread."""
        filepath = self.encode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a file to encode first.")
            return
        
        thread = threading.Thread(target=self.run_encoding, args=(filepath,))
        thread.daemon = True
        thread.start()
        self.set_buttons_state(tk.DISABLED)
    
    def start_decoding_thread(self):
        """Start decoding in a separate thread."""
        filepath = self.decode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a video to decode first.")
            return
        
        thread = threading.Thread(target=self.run_decoding, args=(filepath,))
        thread.daemon = True
        thread.start()
        self.set_buttons_state(tk.DISABLED)
    
    def run_encoding(self, filepath):
        """Run the encoding process."""
        try:
            output_filename = self.encoder.encode_file(filepath)
            messagebox.showinfo("Success", f"Encoding complete!\nVideo saved as {output_filename}")
        except Exception as e:
            messagebox.showerror("Encoding Failed", f"An error occurred: {e}")
        finally:
            self.set_buttons_state(tk.NORMAL)
    
    def run_decoding(self, filepath):
        """Run the decoding process."""
        try:
            output_filename = self.decoder.decode_video(filepath)
            messagebox.showinfo("Success", f"Decoding complete!\nFile saved as {output_filename}")
        except Exception as e:
            messagebox.showerror("Decoding Failed", f"An error occurred: {e}")
        finally:
            self.set_buttons_state(tk.NORMAL)
