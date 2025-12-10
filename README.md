````markdown
# 🧬 Robust Multi-Object Tracking Under Heavy Occlusion

> **Official Research Engine & Dashboard v2.0**
>
> *A Comparative Analysis of Observation-Centric vs. Appearance-Based Methods (DeepOCSORT, StrongSORT, ByteTrack) across DanceTrack, MOT17, and MOT20.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://robustmot.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📄 Abstract
Multi-Object Tracking (MOT) in chaotic environments remains a significant challenge. Standard algorithms often fail when targets undergo **non-linear motion** (e.g., dancing), **heavy occlusion**, or **extreme crowding**.

This thesis benchmarks three state-of-the-art trackers on three diverse datasets:
1.  **DanceTrack:** Complex non-linear motion.
2.  **MOT17:** Standard street surveillance.
3.  **MOT20:** Extreme crowd density.

Our results demonstrate that **DeepOCSORT** offers the optimal trade-off for real-world deployment, achieving **Real-Time speeds (18.5 FPS)** while maintaining competitive accuracy against appearance-heavy baselines.

---

## 🎥 Live Research Dashboard (v2.0)
We have developed a high-performance **interactive dashboard** to visualize the benchmarking results. It features a **Dark Glassmorphism UI**, "Grandmaster" comparison tables, and side-by-side video comparisons.

### **[👉 Click Here to Launch the Live App](https://robustmot.streamlit.app/)**

**Dashboard Features:**
* **Visual Lab:** Compare trackers on 10+ scenarios across 3 datasets.
* **Grandmaster Table:** Side-by-side HOTA/IDF1 metrics for DanceTrack, MOT17, and MOT20.
* **Deep Dive:** Interactive analysis of Occlusion handling and ReID stability.

---

## 🏆 Key Results (DanceTrack Focus)

| Tracker | HOTA (Accuracy) | ID Switches (Stability) | FPS (A100 GPU) | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **StrongSORT** | 🥇 **42.20%** | 2,580 | 6.5 | *Accurate but Slow* |
| **DeepOCSORT** | 🥈 39.39% | 🥇 **1,686 (Best)** | **18.5** | ✅ **Optimal** |
| **ByteTrack** | 🥉 38.21% | 2,241 | 🥇 **43.5** | *Unstable in Occlusion* |

<p align="center">
  <img src="assets/v2.0/Figure_4_Speed_vs_Accuracy.png" width="700" alt="Speed vs Accuracy Trade-off">
  <br>
  <em>Figure 1: The Pareto Frontier. DeepOCSORT (Orange X) occupies the "Sweet Spot" between speed and accuracy.</em>
</p>

---

## 🔬 Reproducibility & Research Code

This repository contains the full "Research Engine" required to reproduce the thesis results from scratch.

### 1. Setup
Download the [DanceTrack Validation Set](https://dancetrack.github.io/) and extract it into a folder named `dancetrack_val_local` in the root directory.

### 2. Run the Benchmark
Execute the scripts in the `research_code/` folder to generate results:

```bash
# 1. Run Inference (Requires GPU)
# Runs trackers on the validation set and saves raw labels.
python research_code/main_benchmark.py

# 2. Standardization
# Converts raw outputs to MOTChallenge format and generates seqmaps.
python research_code/stitch_results.py

# 3. Evaluation
# Patches TrackEval for Numpy 2.0 and calculates HOTA/IDF1 scores.
python research_code/evaluate_results.py

# 4. Visualization
# Generates the figures found in the 'assets/' folder.
python research_code/visualize_plots.py
````

-----

## 🚀 Dashboard Installation (Local)

To run the Streamlit dashboard locally on your machine:

```bash
# 1. Clone the Repo
git clone [https://github.com/smri29/RobustMOTOcclusion.git](https://github.com/smri29/RobustMOTOcclusion.git)
cd RobustMOTOcclusion

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run the App
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

-----

## 📂 Repository Structure

```text
RobustMOTOcclusion/
├── 📄 app.py                  # Main Streamlit Dashboard application
├── 📄 requirements.txt        # Dependencies (streamlit, plotly, pandas, etc.)
├── 📂 assets/
│   └── 📂 v2.0/               # Generated figures (HOTA, Radar Charts, Filmstrips)
├── 📂 research_code/          # Core Python scripts for reproducibility
│   ├── 📄 main_benchmark.py   # Inference engine
│   ├── 📄 evaluate_results.py # HOTA calculation
│   └── 📄 ...
└── 📄 README.md               # Documentation
```

-----

## 📜 Citation

If you use this code or analysis, please cite:

```bibtex
@thesis{Rizvi2025MOT,
  title={Robust Multi-Object Tracking Under Heavy Occlusion},
  author={Shah Mohammad Rizvi and Rume Akter},
  school={IUBAT},
  year={2025}
}
```

## 👥 Authors

  * **Shah Mohammad Rizvi** ([LinkedIn](https://www.linkedin.com/in/smri29/))
  * **Rume Akter**
  * **Supervisor:** Dr. Md. Abdul Awal (Associate Professor, IUBAT)

-----

*Developed with ❤️ using Python, Streamlit, Plotly, and YOLOv8.*

```
```