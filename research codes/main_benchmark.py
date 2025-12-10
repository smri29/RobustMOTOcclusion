import os
import shutil
import subprocess
import sys
import cv2
import numpy as np
import torch
from pathlib import Path
from tqdm import tqdm
from ultralytics import YOLO

# --- DYNAMIC IMPORTS ---
try:
    from boxmot.trackers.bytetrack.bytetrack import ByteTrack
    from boxmot.trackers.deepocsort.deepocsort import DeepOcSort
    from boxmot.trackers.strongsort.strongsort import StrongSort
except ImportError:
    print("⚠️ Standard import failed. Trying fallback to top-level boxmot...")
    try:
        from boxmot import ByteTrack, DeepOcSort, StrongSort
    except ImportError:
         print("❌ Critical: Could not import trackers from boxmot. Ensure 'boxmot' is installed.")
         sys.exit(1)

# --- CONFIGURATION ---
# NOTE: Ensure you have downloaded the DanceTrack validation set into 'dancetrack_val_local'
VAL_DATA_DIR = "dancetrack_val_local"
OUTPUT_DIR = "runs"
MODEL_WEIGHTS = "yolov8x.pt"
REID_WEIGHTS = Path("weights/osnet_x0_25_msmt17.pt")

def download_weights():
    """Downloads ReID weights if they don't exist."""
    if not REID_WEIGHTS.exists():
        REID_WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
        print("⬇️ Downloading ReID weights...")
        try:
            subprocess.run(["wget", "-O", str(REID_WEIGHTS), "https://huggingface.co/paulosantiago/osnet_x0_25_msmt17/resolve/main/osnet_x0_25_msmt17.pt"], check=True)
            print("✅ Weights downloaded.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download weights: {e}")
            sys.exit(1)

def run_benchmark():
    """Runs the tracking benchmark."""
    device = 0 if torch.cuda.is_available() else "cpu"
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    print(f"🚀 Starting Benchmark on: {device_name}")
    
    # 1. Setup
    download_weights()
    model = YOLO(MODEL_WEIGHTS)
    
    if os.path.exists(OUTPUT_DIR): 
        shutil.rmtree(OUTPUT_DIR)

    if not os.path.exists(VAL_DATA_DIR):
        print(f"❌ Dataset not found at {VAL_DATA_DIR}. Please download DanceTrack Val set and extract it there.")
        sys.exit(1)

    sequences = sorted([d for d in os.listdir(VAL_DATA_DIR) if os.path.isdir(os.path.join(VAL_DATA_DIR, d))])

    # 2. Tracker Config
    TRACKER_CONFIGS = {
        "deepocsort": {
            "class": DeepOcSort,
            "args": {"reid_weights": REID_WEIGHTS, "device": device, "half": True, "det_thresh": 0.3}
        },
        "strongsort": {
            "class": StrongSort,
            "args": {"reid_weights": REID_WEIGHTS, "device": device, "half": True, "det_thresh": 0.3}
        },
        "bytetrack": {
            "class": ByteTrack,
            "args": {"track_thresh": 0.25, "match_thresh": 0.8, "track_buffer": 30, "frame_rate": 30}
        }
    }

    # 3. Execution Loop
    for tracker_name, config in TRACKER_CONFIGS.items():
        print(f"\n🏎️  RUNNING: {tracker_name.upper()}")
        tracker_class = config["class"]
        tracker_args = config["args"]
        
        for seq in tqdm(sequences, desc=f"Processing {tracker_name}"):
            try:
                # Re-initialize tracker for each sequence to clear memory/state
                tracker = tracker_class(**tracker_args)
            except Exception as e:
                print(f"❌ Init Error for {tracker_name}: {e}")
                break
            
            seq_path = os.path.join(VAL_DATA_DIR, seq, "img1")
            save_dir = os.path.join(OUTPUT_DIR, tracker_name, seq, "labels")
            os.makedirs(save_dir, exist_ok=True)
            
            frames = sorted([f for f in os.listdir(seq_path) if f.endswith('.jpg')])
            
            for frame_name in frames:
                img_path = os.path.join(seq_path, frame_name)
                img = cv2.imread(img_path)
                
                # Detect
                results = model.predict(img, classes=[0], verbose=False, conf=0.3, device=device)[0]
                dets = results.boxes.data.cpu().numpy() if results.boxes else np.empty((0, 6))
                
                # Update Tracker
                # BoxMOT trackers expect dets and the image
                tracks = tracker.update(dets, img)
                
                # Save Results in MOT format (for now storing normalized YOLO-like lines, will be stitched later)
                if len(tracks) > 0:
                    out_file = os.path.join(save_dir, f"{frame_name.replace('.jpg', '.txt')}")
                    h, w, _ = img.shape
                    with open(out_file, 'w') as f:
                        for t in tracks:
                            # Format: x1, y1, x2, y2, id, conf, class_id, ...
                            x1, y1, x2, y2 = t[:4]
                            tid = int(t[4])
                            
                            # Normalize for intermediate storage (optional, but consistent with your previous flow)
                            x_c = ((x1 + x2)/2) / w
                            y_c = ((y1 + y2)/2) / h
                            w_n = (x2 - x1) / w
                            h_n = (y2 - y1) / h
                            
                            # class_id is usually 0 for pedestrian
                            f.write(f"0 {x_c:.6f} {y_c:.6f} {w_n:.6f} {h_n:.6f} {tid}\n")

    print("\n✅✅ BENCHMARK COMPLETE!")

if __name__ == "__main__":
    run_benchmark()