import cv2
import os

def extract_frames_from_video(video_path, output_folder, max_frames=None):
    """Extract frames from video and save as PNG files"""
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []
    
    frame_count = 0
    saved_frames = []
    
    print(f"Extracting frames from {video_path}...")
    
    while True:
        success, frame = video.read()
        
        if not success:
            break
        
        # Save frame as PNG
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)
        saved_frames.append(frame_filename)
        
        print(f"Saved frame {frame_count}")
        frame_count += 1
        
        # Stop if we've reached max_frames
        if max_frames and frame_count >= max_frames:
            break
    
    video.release()
    print(f"Extracted {frame_count} frames to {output_folder}")
    
    return saved_frames

if __name__ == "__main__":
    video_path = "Diseño sin título.mp4"
    output_folder = "animation_frames"
    
    frames = extract_frames_from_video(video_path, output_folder)
    print(f"Total frames extracted: {len(frames)}")
