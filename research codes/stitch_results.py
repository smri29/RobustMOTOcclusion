import os
import glob
import configparser
from tqdm import tqdm
import shutil

RUNS_DIR = "runs"
OUTPUT_DIR = "tracker_results"
DATASET_DIR = "dancetrack_val_local"

def get_resolution(seq_name):
    """Reads sequence resolution from seqinfo.ini."""
    ini_path = os.path.join(DATASET_DIR, seq_name, "seqinfo.ini")
    if os.path.exists(ini_path):
        config = configparser.ConfigParser()
        config.read(ini_path)
        try:
            return int(config['Sequence']['imWidth']), int(config['Sequence']['imHeight'])
        except KeyError:
            pass
    return 1920, 1080  # Default fallback

def stitch():
    print("🧵 Starting Data Standardization...")
    if os.path.exists(OUTPUT_DIR): 
        shutil.rmtree(OUTPUT_DIR)

    if not os.path.exists(RUNS_DIR):
        print(f"❌ Runs directory '{RUNS_DIR}' not found. Did you run main_benchmark.py?")
        return

    for tracker_folder in os.listdir(RUNS_DIR):
        # Map folder names to paper names
        if "deepoc" in tracker_folder: paper_name = "DeepOCSORT"
        elif "strong" in tracker_folder: paper_name = "StrongSORT"
        elif "byte" in tracker_folder: paper_name = "ByteTrack"
        else: continue 
        
        save_path = os.path.join(OUTPUT_DIR, paper_name, "data")
        os.makedirs(save_path, exist_ok=True)
        
        source_path = os.path.join(RUNS_DIR, tracker_folder)
        video_folders = sorted(os.listdir(source_path))
        
        print(f"📂 Formatting data for: {paper_name}...")
        
        for seq in tqdm(video_folders):
            labels_dir = os.path.join(source_path, seq, "labels")
            if not os.path.exists(labels_dir): continue
                
            img_w, img_h = get_resolution(seq)
            output_file = os.path.join(save_path, f"{seq}.txt")
            
            with open(output_file, 'w') as out_f:
                files = sorted(glob.glob(os.path.join(labels_dir, "*.txt")))
                for f_path in files:
                    try:
                        frame_id = int(os.path.basename(f_path).split('.')[0])
                        # Handle potential leading zeros in filenames if they match frame number
                    except ValueError:
                         continue

                    with open(f_path, 'r') as in_f:
                        for line in in_f:
                            parts = line.strip().split()
                            if len(parts) < 6: continue
                            
                            # Read normalized values
                            xc, yc, w, h = map(float, parts[1:5])
                            tid = int(float(parts[5]))
                            
                            # Convert back to absolute coordinates for MOT format
                            x1 = (xc - w/2) * img_w
                            y1 = (yc - h/2) * img_h
                            ww = w * img_w
                            hh = h * img_h
                            
                            # MOT Challenge Format: <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
                            out_f.write(f"{frame_id},{tid},{x1:.2f},{y1:.2f},{ww:.2f},{hh:.2f},1,-1,-1,-1\n")

    # Generate Seqmap for evaluation
    if os.path.exists(DATASET_DIR):
        os.makedirs(os.path.join(OUTPUT_DIR, "seqmaps"), exist_ok=True)
        with open(os.path.join(OUTPUT_DIR, "seqmaps", "dancetrack-val.txt"), "w") as f:
            f.write("name\n")
            for seq in sorted(os.listdir(DATASET_DIR)):
                if os.path.isdir(os.path.join(DATASET_DIR, seq)):
                    f.write(f"{seq}\n")
    else:
        print(f"⚠️ Dataset directory '{DATASET_DIR}' not found. Skipping seqmap generation.")

    print("✅ Data Standardized.")

if __name__ == "__main__":
    stitch()