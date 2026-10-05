import os
import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT, BLOCK_SIZE, RECONSTRUCTED_PREFIX, FILES_OUTPUT_DIR


class VideoDecoder:
    """Handles decoding video back to file format."""
    
    def __init__(self, logger=None):
        self.logger = logger
    
    def log_message(self, message):
        """Log message if logger is available."""
        if self.logger:
            self.logger(message)
    
    def video_to_frames(self, video_path):
        """Extract frames from video file."""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        self.log_message(f"Extracted {len(frames)} frames.")
        return frames
    
    def frames_to_binary(self, frames):
        """Convert frames back to binary string."""
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
        """Reconstruct file from binary payload."""
        header_str = ""
        i = 0
        
        # Parse header
        while '|' not in header_str or header_str.count('|') < 2:
            header_str += chr(int(binary_payload[i:i+8], 2))
            i += 8
        
        parts = header_str.split('|')
        os.makedirs(FILES_OUTPUT_DIR, exist_ok=True)
        filename = os.path.join(FILES_OUTPUT_DIR, RECONSTRUCTED_PREFIX + parts[0])
        bit_count = int(parts[1])
        
        self.log_message(f"Header parsed. Reconstructing '{filename}'...")
        
        # Extract data
        data_binary = binary_payload[i : i + bit_count]
        byte_array = bytearray(int(data_binary[j:j+8], 2) for j in range(0, len(data_binary), 8))
        
        # Write file
        with open(filename, 'wb') as f:
            f.write(byte_array)
        
        self.log_message(f"✅ Decoding complete! File saved as {filename}")
        return filename
    
    def decode_video(self, video_path):
        """Complete decoding process: video -> file."""
        try:
            self.log_message("--- Starting Decoding Process ---")
            
            # 1. Extract frames from video
            self.log_message("Step 1: Extracting frames from video...")
            frames = self.video_to_frames(video_path)
            
            # 2. Convert frames to binary
            self.log_message("Step 2: Converting frames back to binary data...")
            binary_data = self.frames_to_binary(frames)
            
            # 3. Reconstruct the file
            self.log_message("Step 3: Reconstructing file from binary payload...")
            filename = self.reconstruct_file_from_payload(binary_data)
            
            return filename
            
        except Exception as e:
            self.log_message(f"ERROR: {e}")
            raise e
