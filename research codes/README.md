## 🔬 Reproducibility & Research Code

This repository contains the full "Research Engine" required to reproduce the thesis results.

### 1. Setup
Download the [DanceTrack Validation Set](https://dancetrack.github.io/) and extract it into a folder named `dancetrack_val_local` in the root directory.

### 2. Run the Benchmark
Execute the scripts in order to generate results from scratch:

```bash
# 1. Run the Trackers (Requires GPU)
python research_code/main_benchmark.py

# 2. Convert Results to MOT Format
python research_code/stitch_results.py

# 3. Calculate HOTA Scores
python research_code/evaluate_results.py

# 4. Generate Figures
python research_code/visualize_plots.py