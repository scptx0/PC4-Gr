import cv2
import os

def extract_frames_from_video(video_path, output_folder, max_frames=None):
    """Extract frames from video and save as PNG files"""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
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
        
        # Hacer fondo transparente
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        _, mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)
        
        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
        frame_bgra[:, :, 3] = mask
        
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame_bgra)
        saved_frames.append(frame_filename)
        
        print(f"Saved frame {frame_count}")
        frame_count += 1
        
        if max_frames and frame_count >= max_frames:
            break
    
    video.release()
    print(f"Extracted {frame_count} frames to {output_folder}")
    
    return saved_frames

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    video_path = os.path.join(script_dir, "video.mp4")
    
    src_dir = os.path.dirname(script_dir)
    project_root = os.path.dirname(src_dir)
    output_folder = os.path.join(project_root, "assets", "images", "animation_frames")
    
    print(f"Video path: {video_path}")
    print(f"Output folder: {output_folder}")
    
    frames = extract_frames_from_video(video_path, output_folder)
    print(f"Total frames extracted: {len(frames)}")
