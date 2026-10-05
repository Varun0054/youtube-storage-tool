# YouTube Storage Tool

**Author:** Varun Bhagwat

A tool for encoding files into video format and decoding them back. This allows storing files as videos that can be uploaded to platforms like YouTube.

## Project Structure (MVC)

The project follows the **Model-View-Controller (MVC)** architecture:

```
YtStorage/
├── main.py                          # Entry point — wires View + Controller
├── config.py                        # Configuration constants
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── youtube_storage_original.py      # Original monolithic file (backup)
│
├── models/                          # MODEL — business logic & data processing
│   ├── __init__.py
│   ├── encoder.py                   # VideoEncoder: file → video
│   └── decoder.py                   # VideoDecoder: video → file
│
├── views/                           # VIEW — UI layout & display only
│   ├── __init__.py
│   └── main_view.py                 # MainView (Tkinter window)
│
├── controllers/                     # CONTROLLER — event handling & wiring
│   ├── __init__.py
│   └── app_controller.py            # AppController: connects View ↔ Model
│
└── output/                          # Generated files (git-ignored, folders tracked)
    ├── videos/                      # Encoded videos saved here
    │   └── .gitkeep
    └── files/                       # Decoded/reconstructed files saved here
        └── .gitkeep
```

### MVC Responsibilities

| Layer | Location | Responsibility |
|---|---|---|
| **Model** | `models/` | Encoding/decoding logic, file I/O, OpenCV operations |
| **View** | `views/` | UI layout, widgets, display — zero business logic |
| **Controller** | `controllers/` | Handles button events, threading, calls Model, updates View |

## Features

- **File to Video Encoding**: Convert any file into a video format
- **Video to File Decoding**: Extract files from encoded videos
- **Clean GUI**: User-friendly interface with progress logging
- **MVC Architecture**: Cleanly separated concerns for maintainability
- **Organised Output**: Encoded videos → `output/videos/`, decoded files → `output/files/`
- **Threaded Processing**: UI stays responsive during long operations

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Encode a file**:
   - Click **Browse...** next to *File to Encode*
   - Select any file
   - Click **▶️ Start Encoding**
   - Encoded video is saved to `output/videos/`

2. **Decode a video**:
   - Click **Browse...** next to *Video to Decode*
   - Select an encoded `.mp4` video
   - Click **◀️ Start Decoding**
   - Reconstructed file is saved to `output/files/`

## How It Works

1. **Encoding Process**:
   - File → Binary data (with filename + size header)
   - Binary data → Visual frames (white block = 1, black block = 0)
   - Frames → MP4 video saved to `output/videos/`

2. **Decoding Process**:
   - MP4 video → Extract frames
   - Frames → Binary data
   - Binary data → Parse header → Reconstruct original file → save to `output/files/`

## Configuration

Edit `config.py` to modify:

| Constant | Default | Description |
|---|---|---|
| `FRAME_WIDTH` | `1280` | Video frame width (px) |
| `FRAME_HEIGHT` | `720` | Video frame height (px) |
| `BLOCK_SIZE` | `10` | Pixel block size per bit |
| `FPS` | `30` | Video frame rate |
| `VIDEO_CODEC` | `mp4v` | OpenCV video codec |
| `VIDEOS_OUTPUT_DIR` | `output/videos` | Where encoded videos are saved |
| `FILES_OUTPUT_DIR` | `output/files` | Where decoded files are saved |

## Technical Details

- Uses **OpenCV** for video reading/writing
- Stores metadata (filename, bit-length) in a binary header at the start of the video
- Supports **any file type** (binary-level encoding)
- Processing runs in a **background thread** to keep the UI responsive
