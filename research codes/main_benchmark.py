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
    print("⚠️ Standard import failed. Trying fallback...")
    from boxmot import ByteTrack, DeepOcSort, StrongSort

# --- CONFIGURATION ---
# NOTE: Ensure you have downloaded the DanceTrack validation set into 'dancetrack_val_local'
VAL_DATA_DIR = "dancetrack_val_local"
OUTPUT_DIR = "runs"
MODEL_WEIGHTS = "yolov8x.pt"
REID_WEIGHTS = Path("weights/osnet_x0_25_msmt17.pt")

def download_weights():
    if not REID_WEIGHTS.exists():
        REID_WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
        print("⬇️ Downloading ReID weights...")
        subprocess.run(["wget", "-O", str(REID_WEIGHTS), "https://huggingface.co/paulosantiago/osnet_x0_25_msmt17/resolve/main/osnet_x0_25_msmt17.pt"], check=True)
        print("✅ Weights downloaded.")

def run_benchmark():
    print(f"🚀 Starting Benchmark on GPU: {torch.cuda.get_device_name(0)}")
    
    # 1. Setup
    download_weights()
    model = YOLO(MODEL_WEIGHTS)
    
    if os.path.exists(OUTPUT_DIR): 
        shutil.rmtree(OUTPUT_DIR)

    if not os.path.exists(VAL_DATA_DIR):
        raise FileNotFoundError(f"❌ Dataset not found at {VAL_DATA_DIR}. Please download DanceTrack Val set.")

    sequences = sorted(os.listdir(VAL_DATA_DIR))

    # 2. Tracker Config
    TRACKER_CONFIGS = {
        "deepocsort": {
            "class": DeepOcSort,
            "args": {"reid_weights": REID_WEIGHTS, "device": 0, "half": True, "det_thresh": 0.3}
        },
        "strongsort": {
            "class": StrongSort,
            "args": {"reid_weights": REID_WEIGHTS, "device": 0, "half": True, "det_thresh": 0.3}
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
                tracker = tracker_class(**tracker_args)
            except Exception as e:
                print(f"❌ Init Error: {e}"); break
            
            seq_path = os.path.join(VAL_DATA_DIR, seq, "img1")
            save_dir = os.path.join(OUTPUT_DIR, tracker_name, seq, "labels")
            os.makedirs(save_dir, exist_ok=True)
            
            frames = sorted([f for f in os.listdir(seq_path) if f.endswith('.jpg')])
            
            for frame_name in frames:
                img = cv2.imread(os.path.join(seq_path, frame_name))
                
                # Detect
                results = model.predict(img, classes=[0], verbose=False, conf=0.3, device=0)[0]
                dets = results.boxes.data.cpu().numpy() if results.boxes else np.empty((0, 6))
                
                # Update
                tracks = tracker.update(dets, img)
                
                # Save
                if len(tracks) > 0:
                    out_file = os.path.join(save_dir, f"{frame_name.replace('.jpg', '.txt')}")
                    h, w, _ = img.shape
                    with open(out_file, 'w') as f:
                        for t in tracks:
                            x1, y1, x2, y2 = t[:4]
                            tid = int(t[4])
                            x_c = ((x1 + x2)/2) / w
                            y_c = ((y1 + y2)/2) / h
                            w_n = (x2 - x1) / w
                            h_n = (y2 - y1) / h
                            f.write(f"0 {x_c:.6f} {y_c:.6f} {w_n:.6f} {h_n:.6f} {tid}\n")

    print("\n✅✅ BENCHMARK COMPLETE!")

if __name__ == "__main__":
    run_benchmark()