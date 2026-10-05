import os
import cv2
import numpy as np
from config import FRAME_WIDTH, FRAME_HEIGHT, BLOCK_SIZE, FPS, VIDEO_CODEC, STORAGE_SUFFIX, VIDEO_EXTENSION, VIDEOS_OUTPUT_DIR


class VideoEncoder:
    """Handles encoding files to video format."""
    
    def __init__(self, logger=None):
        self.logger = logger
    
    def log_message(self, message):
        """Log message if logger is available."""
        if self.logger:
            self.logger(message)
    
    def file_to_binary(self, filepath):
        """Convert file to binary string."""
        with open(filepath, 'rb') as f:
            return ''.join(format(byte, '08b') for byte in f.read())
    
    def create_payload(self, filepath):
        """Create binary payload with header containing filename and data length."""
        filename = os.path.basename(filepath)
        binary_data = self.file_to_binary(filepath)
        header = f"{filename}|{len(binary_data)}|"
        return ''.join(format(ord(char), '08b') for char in header) + binary_data
    
    def binary_to_frames(self, binary_payload):
        """Convert binary payload to video frames."""
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
        """Write frames to video file."""
        fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)
        out = cv2.VideoWriter(output_filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
    
    def encode_file(self, filepath):
        """Complete encoding process: file -> video."""
        try:
            self.log_message("--- Starting Encoding Process ---")
            os.makedirs(VIDEOS_OUTPUT_DIR, exist_ok=True)
            base_name = f"{os.path.splitext(os.path.basename(filepath))[0]}{STORAGE_SUFFIX}{VIDEO_EXTENSION}"
            output_filename = os.path.join(VIDEOS_OUTPUT_DIR, base_name)
            
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
            
            return output_filename
            
        except Exception as e:
            self.log_message(f"ERROR: {e}")
            raise e
