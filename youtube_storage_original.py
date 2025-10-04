import os
import cv2
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# --- Configuration Constants ---
# These are the same settings from the command-line script
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
BLOCK_SIZE = 10
FPS = 30

# ==============================================================================
# Main Application Class
# ==============================================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Storage Tool")
        self.geometry("600x650")
        
        # --- Variables ---
        self.encode_filepath = tk.StringVar()
        self.decode_filepath = tk.StringVar()

        # --- Create Widgets ---
        self.create_widgets()

    def log_message(self, message):
        """Inserts a message into the status log text widget."""
        self.status_log.config(state=tk.NORMAL)
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.config(state=tk.DISABLED)
        self.status_log.see(tk.END) # Auto-scroll to the bottom
        self.update_idletasks()

    def create_widgets(self):
        """Creates and arranges all the UI elements in the window."""
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Encoding Section ---
        encode_frame = tk.LabelFrame(main_frame, text=" 📁 Encode File to Video ", padx=10, pady=10)
        encode_frame.pack(fill=tk.X, expand=True, pady=(0, 10))

        tk.Label(encode_frame, text="File to Encode:").grid(row=0, column=0, sticky="w", pady=2)
        encode_entry = tk.Entry(encode_frame, textvariable=self.encode_filepath, state="readonly", width=50)
        encode_entry.grid(row=1, column=0, sticky="we")
        
        select_file_btn = tk.Button(encode_frame, text="Browse...", command=self.select_encode_file)
        select_file_btn.grid(row=1, column=1, padx=(5, 0))

        self.start_encode_btn = tk.Button(encode_frame, text="▶️ Start Encoding", command=self.start_encoding_thread)
        self.start_encode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")

        # --- Decoding Section ---
        decode_frame = tk.LabelFrame(main_frame, text=" 🎥 Decode Video to File ", padx=10, pady=10)
        decode_frame.pack(fill=tk.X, expand=True, pady=10)
        
        tk.Label(decode_frame, text="Video to Decode:").grid(row=0, column=0, sticky="w", pady=2)
        decode_entry = tk.Entry(decode_frame, textvariable=self.decode_filepath, state="readonly", width=50)
        decode_entry.grid(row=1, column=0, sticky="we")

        select_video_btn = tk.Button(decode_frame, text="Browse...", command=self.select_decode_video)
        select_video_btn.grid(row=1, column=1, padx=(5, 0))

        self.start_decode_btn = tk.Button(decode_frame, text="◀️ Start Decoding", command=self.start_decoding_thread)
        self.start_decode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")
        
        # --- Status Log Section ---
        log_frame = tk.LabelFrame(main_frame, text=" 📊 Status Log ", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_log = scrolledtext.ScrolledText(log_frame, state="disabled", height=10, wrap=tk.WORD)
        self.status_log.pack(fill=tk.BOTH, expand=True)

    def select_encode_file(self):
        """Opens a file dialog to select a file for encoding."""
        filepath = filedialog.askopenfilename(title="Select a file to encode")
        if filepath:
            self.encode_filepath.set(filepath)
            self.log_message(f"Selected for encoding: {os.path.basename(filepath)}")

    def select_decode_video(self):
        """Opens a file dialog to select a video for decoding."""
        filepath = filedialog.askopenfilename(
            title="Select a video to decode",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*"))
        )
        if filepath:
            self.decode_filepath.set(filepath)
            self.log_message(f"Selected for decoding: {os.path.basename(filepath)}")

    def set_buttons_state(self, state):
        """Disables or enables the start buttons to prevent multiple operations."""
        self.start_encode_btn.config(state=state)
        self.start_decode_btn.config(state=state)

    # --- Threading Wrappers ---
    def start_encoding_thread(self):
        filepath = self.encode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a file to encode first.")
            return
        
        # Run the encoding process in a separate thread to keep the UI responsive
        thread = threading.Thread(target=self.run_encoding, args=(filepath,))
        thread.daemon = True
        thread.start()
        self.set_buttons_state(tk.DISABLED)

    def start_decoding_thread(self):
        filepath = self.decode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a video to decode first.")
            return

        thread = threading.Thread(target=self.run_decoding, args=(filepath,))
        thread.daemon = True
        thread.start()
        self.set_buttons_state(tk.DISABLED)

    # ==============================================================================
    # Backend Logic (from the previous script)
    # ==============================================================================

    def run_encoding(self, filepath):
        """The complete encoding process."""
        try:
            self.log_message("--- Starting Encoding Process ---")
            output_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}_storage.mp4"

            # 1. Create payload
            self.log_message("Step 1: Creating data payload with header...")
            binary_payload = self.create_payload(filepath)
            self.log_message("Payload created successfully.")

            # 2. Convert to frames
            self.log_message("Step 2: Converting binary data to visual frames...")
            frames = self.binary_to_frames(binary_payload)
            self.log_message("Frame generation complete.")

            # 3. Write to video
            self.log_message(f"Step 3: Writing frames to '{output_filename}'...")
            self.frames_to_video(frames, output_filename)
            self.log_message(f"✅ Encoding complete! Video saved as {output_filename}")
            messagebox.showinfo("Success", f"Encoding complete!\nVideo saved as {output_filename}")

        except Exception as e:
            self.log_message(f"ERROR: {e}")
            messagebox.showerror("Encoding Failed", f"An error occurred: {e}")
        finally:
            self.set_buttons_state(tk.NORMAL)

    def run_decoding(self, filepath):
        """The complete decoding process."""
        try:
            self.log_message("--- Starting Decoding Process ---")

            # 1. Extract frames from video
            self.log_message("Step 1: Extracting frames from video...")
            frames = self.video_to_frames(filepath)
            
            # 2. Convert frames to binary
            self.log_message("Step 2: Converting frames back to binary data...")
            binary_data = self.frames_to_binary(frames)

            # 3. Reconstruct the file
            self.log_message("Step 3: Reconstructing file from binary payload...")
            self.reconstruct_file_from_payload(binary_data)

        except Exception as e:
            self.log_message(f"ERROR: {e}")
            messagebox.showerror("Decoding Failed", f"An error occurred: {e}")
        finally:
            self.set_buttons_state(tk.NORMAL)

    # --- Backend Helper Functions ---
    def file_to_binary(self, filepath):
        with open(filepath, 'rb') as f:
            return ''.join(format(byte, '08b') for byte in f.read())

    def create_payload(self, filepath):
        filename = os.path.basename(filepath)
        binary_data = self.file_to_binary(filepath)
        header = f"{filename}|{len(binary_data)}|"
        return ''.join(format(ord(char), '08b') for char in header) + binary_data

    def binary_to_frames(self, binary_payload):
        blocks_per_row = FRAME_WIDTH // BLOCK_SIZE
        bits_per_frame = (FRAME_WIDTH // BLOCK_SIZE) * (FRAME_HEIGHT // BLOCK_SIZE)
        frames = []
        total_frames = (len(binary_payload) + bits_per_frame - 1) // bits_per_frame
        
        for i in range(0, len(binary_payload), bits_per_frame):
            chunk = binary_payload[i:i+bits_per_frame]
            frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
            for bit_index, bit in enumerate(chunk):
                if bit == '1':
                    row = (bit_index // blocks_per_row) * BLOCK_SIZE
                    col = (bit_index % blocks_per_row) * BLOCK_SIZE
                    cv2.rectangle(frame, (col, row), (col + BLOCK_SIZE, row + BLOCK_SIZE), (255, 255, 255), -1)
            frames.append(frame)
            self.log_message(f"Generated frame {len(frames)}/{total_frames}...")
        return frames

    def frames_to_video(self, frames, output_filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        for frame in frames:
            out.write(frame)
        out.release()
    
    def video_to_frames(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret: break
            frames.append(frame)
        cap.release()
        self.log_message(f"Extracted {len(frames)} frames.")
        return frames

    def frames_to_binary(self, frames):
        binary_string = ""
        total_frames = len(frames)
        for frame_num, frame in enumerate(frames):
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for r in range(0, FRAME_HEIGHT, BLOCK_SIZE):
                for c in range(0, FRAME_WIDTH, BLOCK_SIZE):
                    if r + BLOCK_SIZE <= FRAME_HEIGHT and c + BLOCK_SIZE <= FRAME_WIDTH:
                        pixel_value = gray_frame[r + BLOCK_SIZE // 2, c + BLOCK_SIZE // 2]
                        binary_string += '1' if pixel_value > 127 else '0'
            self.log_message(f"Processed frame {frame_num + 1}/{total_frames}...")
        return binary_string
    
    def reconstruct_file_from_payload(self, binary_payload):
        header_str = ""
        i = 0
        while '|' not in header_str or header_str.count('|') < 2:
            header_str += chr(int(binary_payload[i:i+8], 2))
            i += 8
        
        parts = header_str.split('|')
        filename = "reconstructed_" + parts[0]
        bit_count = int(parts[1])
        self.log_message(f"Header parsed. Reconstructing '{filename}'...")
        
        data_binary = binary_payload[i : i + bit_count]
        byte_array = bytearray(int(data_binary[j:j+8], 2) for j in range(0, len(data_binary), 8))

        with open(filename, 'wb') as f:
            f.write(byte_array)
        
        self.log_message(f"✅ Decoding complete! File saved as {filename}")
        messagebox.showinfo("Success", f"Decoding complete!\nFile saved as {filename}")


if __name__ == "__main__":
    app = App()
    app.mainloop()