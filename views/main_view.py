import tkinter as tk
from tkinter import filedialog, scrolledtext


class MainView(tk.Tk):
    """
    View: Responsible only for UI layout and display.
    All event handling is delegated to the Controller via bind_callbacks().
    """

    def __init__(self):
        super().__init__()
        self.title("YouTube Storage Tool")
        self.geometry("600x650")

        # Path variables
        self.encode_filepath = tk.StringVar()
        self.decode_filepath = tk.StringVar()

        self._create_widgets()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _create_widgets(self):
        """Build and arrange all UI elements."""
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_encoding_section(main_frame)
        self._create_decoding_section(main_frame)
        self._create_log_section(main_frame)

    def _create_encoding_section(self, parent):
        encode_frame = tk.LabelFrame(parent, text=" 📁 Encode File to Video ", padx=10, pady=10)
        encode_frame.pack(fill=tk.X, expand=True, pady=(0, 10))

        tk.Label(encode_frame, text="File to Encode:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(encode_frame, textvariable=self.encode_filepath, state="readonly", width=50).grid(row=1, column=0, sticky="we")

        self.select_encode_btn = tk.Button(encode_frame, text="Browse...")
        self.select_encode_btn.grid(row=1, column=1, padx=(5, 0))

        self.start_encode_btn = tk.Button(encode_frame, text="▶️ Start Encoding")
        self.start_encode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")

    def _create_decoding_section(self, parent):
        decode_frame = tk.LabelFrame(parent, text=" 🎥 Decode Video to File ", padx=10, pady=10)
        decode_frame.pack(fill=tk.X, expand=True, pady=10)

        tk.Label(decode_frame, text="Video to Decode:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(decode_frame, textvariable=self.decode_filepath, state="readonly", width=50).grid(row=1, column=0, sticky="we")

        self.select_decode_btn = tk.Button(decode_frame, text="Browse...")
        self.select_decode_btn.grid(row=1, column=1, padx=(5, 0))

        self.start_decode_btn = tk.Button(decode_frame, text="◀️ Start Decoding")
        self.start_decode_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="we")

    def _create_log_section(self, parent):
        log_frame = tk.LabelFrame(parent, text=" 📊 Status Log ", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.status_log = scrolledtext.ScrolledText(log_frame, state="disabled", height=10, wrap=tk.WORD)
        self.status_log.pack(fill=tk.BOTH, expand=True)

    # ── Public display methods (called by Controller) ─────────────────────────

    def bind_callbacks(self, callbacks: dict):
        """Wire controller callbacks to button commands."""
        self.select_encode_btn.config(command=callbacks["select_encode_file"])
        self.start_encode_btn.config(command=callbacks["start_encoding"])
        self.select_decode_btn.config(command=callbacks["select_decode_video"])
        self.start_decode_btn.config(command=callbacks["start_decoding"])

    def log_message(self, message: str):
        """Append a message to the status log."""
        self.status_log.config(state=tk.NORMAL)
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.config(state=tk.DISABLED)
        self.status_log.see(tk.END)
        self.update_idletasks()

    def set_buttons_state(self, state):
        """Enable or disable action buttons."""
        self.start_encode_btn.config(state=state)
        self.start_decode_btn.config(state=state)

    def ask_encode_file(self):
        """Open file picker and return selected path (or empty string)."""
        return filedialog.askopenfilename(title="Select a file to encode")

    def ask_decode_file(self):
        """Open file picker for video and return selected path (or empty string)."""
        return filedialog.askopenfilename(
            title="Select a video to decode",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov"), ("All files", "*.*")),
        )
