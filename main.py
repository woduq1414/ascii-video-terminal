#!/usr/bin/env python3
"""
🐦 ASCII Terminal Parrot Server
Python implementation of parrot.live - bringing animated parrots to terminals everywhere!
"""
import time
import re
import os
import glob
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# ANSI color codes
RESET = '\033[0m'
BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'

# Clear screen and cursor control
CLEAR_SCREEN = '\033[2J\033[H'  # Clear entire screen and move cursor to home
CLEAR_LINE = '\033[2K'          # Clear entire line
HIDE_CURSOR = '\033[?25l'       # Hide cursor
SHOW_CURSOR = '\033[?25h'       # Show cursor
MOVE_UP = '\033[A'              # Move cursor up one line
MOVE_HOME = '\033[H'            # Move cursor to home position

def load_frame_files(folder_name="overdrive"):
    """Load animation frames from files in the specified folder"""
    frames_dir = f"saved_frames/{folder_name}"
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.txt")))
    
    frames = []
    colors = [YELLOW, CYAN, RED, GREEN, MAGENTA, BLUE]
    
    for i, frame_file in enumerate(frame_files):
        try:
            with open(frame_file, 'r', encoding='utf-8') as f:
                frame_content = f.read()
                # Apply color to each frame
                color = colors[i % len(colors)]
                colored_frame = f"{color}{frame_content}{RESET}"
                frames.append(colored_frame)
        except FileNotFoundError:
            print(f"Warning: Frame file {frame_file} not found")
        except Exception as e:
            print(f"Error loading frame {frame_file}: {e}")
    
    # Fallback to a simple frame if no files are found
    if not frames:
        frames = [f"{GREEN}🐦 No frames found in '{folder_name}' directory! 🐦{RESET}"]
    
    return frames

def get_available_folders():
    """Get list of available animation folders"""
    saved_frames_dir = "saved_frames"
    if not os.path.exists(saved_frames_dir):
        return []
    
    folders = []
    for item in os.listdir(saved_frames_dir):
        item_path = os.path.join(saved_frames_dir, item)
        if os.path.isdir(item_path):
            # Check if folder contains frame files
            frame_files = glob.glob(os.path.join(item_path, "frame_*.txt"))
            if frame_files:
                folders.append(item)
    return folders

# Load default parrot animation frames from files
DEFAULT_FRAMES = load_frame_files()

def is_curl_request(user_agent):
    """Check if the request is from curl"""
    if not user_agent:
        return False
    
    return bool(re.search(r'curl|wget|httpie|perl|python|ruby|php|go-http|java|c\+\+|libwww', 
                         user_agent.lower()))

def generate_parrot_animation(frames, folder_name="overdrive", interval=0.1, stride=1):
    """Generate the parrot animation stream"""
    try:
        # Send initial setup - hide cursor and clear screen
        yield HIDE_CURSOR + CLEAR_SCREEN
        
        # Apply stride - select every nth frame
        selected_frames = frames[::stride] if stride > 1 else frames
        
        # Loop the animation forever
        while True:
            for i, frame in enumerate(selected_frames):
                # Clear entire screen more thoroughly
                # ESC[2J - clear entire screen
                # ESC[H - move cursor to home position  
                # ESC[3J - clear scrollback buffer
                clear_sequence = '\033[2J\033[3J\033[H'
                
                # Build complete frame content in one go
                frame_content = clear_sequence
                frame_content += frame + "\n\n"
                frame_content += f"{YELLOW}🎉 Animation '{folder_name}' #{i+1}/{len(selected_frames)} - Use Ctrl+C to stop! 🎉{RESET}\n"
                frame_content += f"{MAGENTA}Interval: {interval}s | Stride: {stride} | Total frames: {len(frames)}{RESET}\n"
                frame_content += f"{RESET}\n"
                
                # Send the complete frame as one chunk
                yield frame_content
                
                # Wait before next frame with custom interval
                time.sleep(interval)
                
    except GeneratorExit:
        # Clean up when client disconnects gracefully
        yield SHOW_CURSOR + CLEAR_SCREEN
        return
    except Exception:
        # Handle any other exceptions gracefully
        yield SHOW_CURSOR + CLEAR_SCREEN
        return

def create_animation_response(frames, folder_name, interval, stride):
    """Create animation response with proper headers"""
    response = Response(
        generate_parrot_animation(frames, folder_name, interval, stride),
        mimetype='text/plain',
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache', 
            'Expires': '0',
            'Connection': 'close',
            'Content-Type': 'text/plain; charset=utf-8'
        }
    )
    return response

@app.route('/')
def index():
    """Main route handler - default overdrive animation"""
    user_agent = request.headers.get('User-Agent', '')
    
    # Check if request is from curl or similar command line tool
    if is_curl_request(user_agent):
        # Get query parameters
        interval = float(request.args.get('interval', 0.1))
        stride = int(request.args.get('stride', 1))
        
        # Validate parameters
        interval = max(0.01, min(interval, 10.0))  # Between 0.01 and 10 seconds
        stride = max(1, min(stride, 100))  # Between 1 and 100
        
        return create_animation_response(DEFAULT_FRAMES, "overdrive", interval, stride)
    else:
        # Redirect browsers to GitHub (like original parrot.live)
        return redirect('https://github.com/woduq1414/ascii-video-terminal', code=302)

@app.route('/<folder_name>')
def folder_animation(folder_name):
    """Animation route for specific folders"""
    user_agent = request.headers.get('User-Agent', '')
    
    # Check if request is from curl or similar command line tool
    if is_curl_request(user_agent):
        # Get query parameters
        interval = float(request.args.get('interval', 0.1))
        stride = int(request.args.get('stride', 1))
        
        # Validate parameters
        interval = max(0.01, min(interval, 10.0))  # Between 0.01 and 10 seconds
        stride = max(1, min(stride, 100))  # Between 1 and 100
        
        # Check if folder exists and has frames
        available_folders = get_available_folders()
        if folder_name not in available_folders:
            error_frames = [f"{RED}❌ Folder '{folder_name}' not found!{RESET}\n\n{YELLOW}Available folders: {', '.join(available_folders)}{RESET}"]
            return create_animation_response(error_frames, folder_name, interval, stride)
        
        # Load frames for the specified folder
        frames = load_frame_files(folder_name)
        return create_animation_response(frames, folder_name, interval, stride)
    else:
        # Redirect browsers to GitHub
        return redirect('https://github.com/hugomd/parrot.live', code=302)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': '🐦 Parrot server is flying!'}

if __name__ == "__main__":
    print(f"{GREEN}🐦 Starting ASCII Terminal Parrot Server...{RESET}")
    print(f"{YELLOW}Try: curl localhost:8081{RESET}")
    print(f"{YELLOW}     curl localhost:8081/overdrive{RESET}")
    print(f"{YELLOW}     curl \"localhost:8081/overdrive?interval=0.2&stride=2\"{RESET}")
    print(f"{CYAN}Or visit http://localhost:8081 in your browser{RESET}")
    print(f"{MAGENTA}Available folders: {', '.join(get_available_folders())}{RESET}")
    
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=False,
        threaded=True
    )
