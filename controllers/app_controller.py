"""
Controller: AppController
Connects the View (MainView) to the Models (VideoEncoder, VideoDecoder).
Handles all user events, threading, and application logic flow.
"""

import os
import threading
import tkinter as tk
from tkinter import messagebox

from models.encoder import VideoEncoder
from models.decoder import VideoDecoder


class AppController:
    """
    Controller that mediates between MainView and the encoder/decoder models.
    Instantiated after the View so it can bind callbacks to UI buttons.
    """

    def __init__(self, view):
        self.view = view

        # Instantiate models — pass the view's log_message as the logger
        self.encoder = VideoEncoder(logger=view.log_message)
        self.decoder = VideoDecoder(logger=view.log_message)

        # Wire button events to controller methods
        self.view.bind_callbacks({
            "select_encode_file": self.select_encode_file,
            "start_encoding":     self.start_encoding_thread,
            "select_decode_video": self.select_decode_video,
            "start_decoding":     self.start_decoding_thread,
        })

    # ── File selection ────────────────────────────────────────────────────────

    def select_encode_file(self):
        """Ask the View to open a file picker, then store the chosen path."""
        filepath = self.view.ask_encode_file()
        if filepath:
            self.view.encode_filepath.set(filepath)
            self.view.log_message(f"Selected for encoding: {os.path.basename(filepath)}")

    def select_decode_video(self):
        """Ask the View to open a video picker, then store the chosen path."""
        filepath = self.view.ask_decode_file()
        if filepath:
            self.view.decode_filepath.set(filepath)
            self.view.log_message(f"Selected for decoding: {os.path.basename(filepath)}")

    # ── Threading wrappers ────────────────────────────────────────────────────

    def start_encoding_thread(self):
        """Validate input, then run encoding in a background thread."""
        filepath = self.view.encode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a file to encode first.")
            return

        self.view.set_buttons_state(tk.DISABLED)
        thread = threading.Thread(target=self._run_encoding, args=(filepath,), daemon=True)
        thread.start()

    def start_decoding_thread(self):
        """Validate input, then run decoding in a background thread."""
        filepath = self.view.decode_filepath.get()
        if not filepath:
            messagebox.showerror("Error", "Please select a video to decode first.")
            return

        self.view.set_buttons_state(tk.DISABLED)
        thread = threading.Thread(target=self._run_decoding, args=(filepath,), daemon=True)
        thread.start()

    # ── Model calls ───────────────────────────────────────────────────────────

    def _run_encoding(self, filepath):
        """Call the encoder model and handle success/failure feedback."""
        try:
            output_filename = self.encoder.encode_file(filepath)
            messagebox.showinfo("Success", f"Encoding complete!\nVideo saved as {output_filename}")
        except Exception as e:
            messagebox.showerror("Encoding Failed", f"An error occurred: {e}")
        finally:
            self.view.set_buttons_state(tk.NORMAL)

    def _run_decoding(self, filepath):
        """Call the decoder model and handle success/failure feedback."""
        try:
            output_filename = self.decoder.decode_video(filepath)
            messagebox.showinfo("Success", f"Decoding complete!\nFile saved as {output_filename}")
        except Exception as e:
            messagebox.showerror("Decoding Failed", f"An error occurred: {e}")
        finally:
            self.view.set_buttons_state(tk.NORMAL)
