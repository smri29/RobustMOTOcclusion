import os
import shutil
import subprocess
import sys

def setup_eval():
    """Clones and patches the TrackEval library for compatibility."""
    if os.path.exists("TrackEval"):
        shutil.rmtree("TrackEval")
    
    print("⬇️ Cloning TrackEval repository...")
    try:
        subprocess.run(["git", "clone", "https://github.com/JonathonLuiten/TrackEval.git", "-q"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone TrackEval: {e}")
        return False

    # APPLY FIXES
    target_file = 'TrackEval/trackeval/datasets/mot_challenge_2d_box.py'
    if os.path.exists(target_file):
        with open(target_file, 'r') as f: content = f.read()
        
        # Fix Numpy 2.0 Compatibility (Deprecation of np.int, np.float, np.bool)
        content = content.replace("np.int", "int").replace("np.float", "float").replace("np.bool", "bool")
        
        # Fix Path Logic for seqmap handling
        if "if not os.path.isfile(seqmap_file):" in content:
            # We use a string replacement that mimics the indentation of the original file
            old = "if not os.path.isfile(seqmap_file):"
            new = "if isinstance(seqmap_file, list): seqmap_file = seqmap_file[0]\n        if not os.path.isfile(seqmap_file):"
            content = content.replace(old, new)

        with open(target_file, 'w') as f: f.write(content)
        print("✅ TrackEval Library Patched.")
    else:
        print(f"⚠️ Could not find {target_file} to patch.")
        return False
    return True

def run_eval():
    """Runs the HOTA evaluation script."""
    print("🏆 Calculating HOTA Scores...")
    
    # Define evaluation parameters
    tracker_results_folder = "tracker_results"
    gt_folder = "dancetrack_val_local"
    seqmap_file = os.path.join(tracker_results_folder, "seqmaps", "dancetrack-val.txt")

    if not os.path.exists(seqmap_file):
        print(f"❌ Seqmap file not found at {seqmap_file}. Did you run stitch_results.py?")
        return

    cmd = (
        f"{sys.executable} TrackEval/scripts/run_mot_challenge.py "
        "--BENCHMARK DanceTrack "
        "--SPLIT_TO_EVAL val "
        "--TRACKERS_TO_EVAL DeepOCSORT StrongSORT ByteTrack "
        "--METRICS HOTA Identity "
        "--USE_PARALLEL False "
        f"--GT_FOLDER {gt_folder} "
        f"--TRACKERS_FOLDER {tracker_results_folder} "
        "--GT_LOC_FORMAT '{gt_folder}/{seq}/gt/gt.txt' "
        "--TRACKER_SUB_FOLDER 'data' "
        "--OUTPUT_SUB_FOLDER '' "
        f"--SEQMAP_FILE {seqmap_file} "
        "--SKIP_SPLIT_FOL True "
        "--CLASSES_TO_EVAL pedestrian "
        "--PRINT_CONFIG False"
    )
    
    try:
        os.system(cmd)
    except Exception as e:
        print(f"❌ Error running evaluation: {e}")

if __name__ == "__main__":
    if setup_eval():
        run_eval()