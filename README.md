# YouTube Storage Tool

**Author:** Varun Bhagwat

A tool for encoding files into video format and decoding them back. This allows storing files as videos that can be uploaded to platforms like YouTube.

## Project Structure

```
YtStorage/
├── main.py                 # Main entry point
├── config.py              # Configuration constants
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── youtube_storage_original.py  # Original monolithic file (backup)
├── core/                 # Core encoding/decoding logic
│   ├── __init__.py
│   ├── encoder.py        # VideoEncoder class
│   └── decoder.py        # VideoDecoder class
└── gui/                  # GUI components
    ├── __init__.py
    └── main_window.py    # MainWindow class
```

## Features

- **File to Video Encoding**: Convert any file into a video format
- **Video to File Decoding**: Extract files from encoded videos
- **Clean GUI**: User-friendly interface with progress logging
- **Modular Design**: Separated concerns for better maintainability

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## How It Works

1. **Encoding Process**:
   - File → Binary data
   - Binary data → Visual frames (white blocks = 1, black = 0)
   - Frames → Video file

2. **Decoding Process**:
   - Video file → Frames
   - Frames → Binary data
   - Binary data → Original file

## Configuration

Edit `config.py` to modify:
- Video resolution (FRAME_WIDTH, FRAME_HEIGHT)
- Block size for binary representation
- Video frame rate
- File naming conventions

## Usage

1. **Encode a file**:
   - Click "Browse..." to select a file
   - Click "▶️ Start Encoding"
   - Wait for the process to complete

2. **Decode a video**:
   - Click "Browse..." to select a video file
   - Click "◀️ Start Decoding"
   - Wait for the process to complete

## Technical Details

- Uses OpenCV for video processing
- Converts files to binary, then to visual patterns
- Stores metadata (filename, size) in video header
- Supports any file type
- Threaded processing to keep UI responsive
