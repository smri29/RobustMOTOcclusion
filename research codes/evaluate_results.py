import os
import shutil
import subprocess

def setup_eval():
    if os.path.exists("TrackEval"): shutil.rmtree("TrackEval")
    subprocess.run(["git", "clone", "https://github.com/JonathonLuiten/TrackEval.git", "-q"])
    
    # APPLY FIXES
    target_file = 'TrackEval/trackeval/datasets/mot_challenge_2d_box.py'
    if os.path.exists(target_file):
        with open(target_file, 'r') as f: content = f.read()
        
        # Fix Numpy 2.0
        content = content.replace("np.int", "int").replace("np.float", "float").replace("np.bool", "bool")
        
        # Fix Path Logic
        if "if not os.path.isfile(seqmap_file):" in content:
            # We use a string replacement that mimics the indentation of the original file
            # Note: This regex-like replace is safer than line insertion
            old = "if not os.path.isfile(seqmap_file):"
            new = "if isinstance(seqmap_file, list): seqmap_file = seqmap_file[0]\n        if not os.path.isfile(seqmap_file):"
            content = content.replace(old, new)

        with open(target_file, 'w') as f: f.write(content)
        print("✅ TrackEval Library Patched.")

def run_eval():
    print("🏆 Calculating HOTA Scores...")
    cmd = (
        "python TrackEval/scripts/run_mot_challenge.py "
        "--BENCHMARK DanceTrack "
        "--SPLIT_TO_EVAL val "
        "--TRACKERS_TO_EVAL DeepOCSORT StrongSORT ByteTrack "
        "--METRICS HOTA Identity "
        "--USE_PARALLEL False "
        "--GT_FOLDER dancetrack_val_local "
        "--TRACKERS_FOLDER tracker_results "
        "--GT_LOC_FORMAT '{gt_folder}/{seq}/gt/gt.txt' "
        "--TRACKER_SUB_FOLDER 'data' "
        "--OUTPUT_SUB_FOLDER '' "
        "--SEQMAP_FILE tracker_results/seqmaps/dancetrack-val.txt "
        "--SKIP_SPLIT_FOL True "
        "--CLASSES_TO_EVAL pedestrian "
        "--PRINT_CONFIG False"
    )
    os.system(cmd)

if __name__ == "__main__":
    setup_eval()
    run_eval()