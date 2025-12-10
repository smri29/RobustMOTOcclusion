## 🔬 Reproducibility & Research Code

This repository contains the full "Research Engine" required to reproduce the thesis results for **Robust Multi-Object Tracking Under Heavy Occlusion**.

### 1. Setup

#### Requirements
* Python 3.8+
* PyTorch (with CUDA support recommended)
* [BoxMOT](https://github.com/mikel-brostrom/yolo_tracking) library
* Ultralytics YOLO

#### Dataset
Download the [DanceTrack Validation Set](https://dancetrack.github.io/) and extract it into a folder named `dancetrack_val_local` in the root directory of this repository.

### 2. Run the Benchmark
Execute the scripts in order to generate results from scratch:

```bash
# 1. Run the Trackers (Requires GPU)
# Runs DeepOCSORT, StrongSORT, and ByteTrack on the validation set.
# Saves raw YOLO-format labels to 'runs/' directory.
python research_code/main_benchmark.py

# 2. Convert Results to MOT Format
# Stitches raw labels into standard MOTChallenge format text files.
# Saves to 'tracker_results/' directory and generates seqmaps.
python research_code/stitch_results.py

# 3. Calculate HOTA Scores
# Clones TrackEval, patches it for compatibility, and runs evaluation.
# Outputs HOTA, DetA, AssA, and IDF1 scores.
python research_code/evaluate_results.py

# 4. Generate Figures
# Visualizes the results as Bar Charts and Scatter Plots.
# Saves images to 'assets/' folder.
python research_code/visualize_plots.py

3. File Descriptions
main_benchmark.py: Core inference script using YOLOv8x and BoxMOT trackers.

stitch_results.py: Data processing utility to convert per-frame outputs to MOT format.

evaluate_results.py: Evaluation wrapper using the official TrackEval kit.

visualize_plots.py: Generates the visual figures used in the thesis report and dashboard.