import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="RobustMOT Thesis Dashboard",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURATION & ASSETS ---
# Base path for assets (Relative to where app.py is running)
ASSET_DIR = os.path.join("assets", "v2.0")

# VIDEO DATABASE
VIDEO_DB = {
    "DanceTrack (Non-Linear Motion)": {
        "ByteTrack": {
            "Seq 04: Heavy Occlusion": "https://youtu.be/fbwpWQks8og", # Assuming this one is correct based on prev context, or replace if specific byte link exists
            "ByteTrack Playlist 1": "https://youtu.be/kjJemGMhZoE",
            "ByteTrack Playlist 2": "https://youtu.be/vULe68-KiKU",
            "ByteTrack Playlist 3": "https://youtu.be/PMH7_GYXMhA",
            "ByteTrack Playlist 4": "https://youtu.be/CCMz_C4B2Yc",
            "ByteTrack Playlist 5": "https://youtu.be/zAaNYtqc7h0"
        },
        "DeepOCSORT": {
             "DeepTrack Playlist 1": "https://youtu.be/PZUw_-a-xYw",
             "DeepTrack Playlist 2": "https://youtu.be/hI_33oCsFFQ",
             "DeepTrack Playlist 3": "https://youtu.be/QYORhr6mR58",
             "DeepTrack Playlist 4": "https://youtu.be/qTP5WZbMUXQ",
             "DeepTrack Playlist 5": "https://youtu.be/hpxe59Pax9s"
        },
        "StrongSORT": {
             "StrongSORT Playlist 1": "https://youtu.be/_R5aXEy_gsw",
             "StrongSORT Playlist 2": "https://youtu.be/urKx9npTrqI",
             "StrongSORT Playlist 3": "https://youtu.be/9zgvI5MX7M4",
             "StrongSORT Playlist 4": "https://youtu.be/GaDQKKdsRBU",
             "StrongSORT Playlist 5": "https://youtu.be/D4PZo9tzEaY"
        }
    },
    "MOT17 (Street Scenes)": {
        "ByteTrack": {
             "ByteTrack Playlist 1": "https://youtu.be/dyebzXCk6U4",
             "ByteTrack Playlist 2": "https://youtu.be/g5vKq6HDorY",
             "ByteTrack Playlist 3": "https://youtu.be/J4qWY9tCcAM",
             "ByteTrack Playlist 4": "https://youtu.be/WC9uqvzXv0M",
             "ByteTrack Playlist 5": "https://youtu.be/zH8p6OQDzuM"
        },
        "DeepOCSORT": {
             "DeepOCSORT Playlist 1": "https://youtu.be/hdYlkSdGUDg",
             "DeepOCSORT Playlist 2": "https://youtu.be/atDdNtv7sIM",
             "DeepOCSORT Playlist 3": "https://youtu.be/uU4D2QhBjAM",
             "DeepOCSORT Playlist 4": "https://youtu.be/Tbi0PGN1bOE",
             "DeepOCSORT Playlist 5": "https://youtu.be/PdCet9NbLFw"
        },
        "StrongSORT": {
             "StrongSORT Playlist 1": "https://youtu.be/jUyDMUkPp2k",
             "StrongSORT Playlist 2": "https://youtu.be/8EKhf1kfN7k",
             "StrongSORT Playlist 3": "https://youtu.be/KbRQu5KwH64",
             "StrongSORT Playlist 4": "https://youtu.be/W364cn6km7I",
             "StrongSORT Playlist 5": "https://youtu.be/LK-VOa5VuGo"
        }
    },
    "MOT20 (Extreme Crowds)": {
        "ByteTrack": {
             "ByteTrack Playlist 1": "https://youtu.be/-GBZP34VVMY",
             "ByteTrack Playlist 2": "https://youtu.be/g6nvFKrjRFE",
             "ByteTrack Playlist 3": "https://youtu.be/TqWX5Gglce4",
             "ByteTrack Playlist 4": "https://youtu.be/wkA2Bdo--Yw"
        },
        "DeepOCSORT": {
             "DeepOCSORT Playlist 1": "https://youtu.be/OHON2YiXwnM",
             "DeepOCSORT Playlist 2": "https://youtu.be/BVMIBzfWCGo",
             "DeepOCSORT Playlist 3": "https://youtu.be/NuZEmdG2e0w",
             "DeepOCSORT Playlist 4": "https://youtu.be/s3wQ0gUr0Hc"
        },
        "StrongSORT": {
             "StrongSORT Playlist 1": "https://youtu.be/CK7eRYm4qkw",
             "StrongSORT Playlist 2": "https://youtu.be/xVDLKGd5wL4",
             "StrongSORT Playlist 3": "https://youtu.be/-O3vqBjKhEM",
             "StrongSORT Playlist 4": "https://youtu.be/45uF8YhjgH8"
        }
    }
}

# EXPERIMENTAL RESULTS DATA
data_dict = {
    "DanceTrack": {
        'Tracker': ['StrongSORT', 'DeepOCSORT', 'ByteTrack'],
        'HOTA': [42.2, 39.4, 38.2],
        'IDF1': [40.4, 37.2, 39.5],
        'DetA': [66.7, 65.7, 61.9],
        'AssA': [27.0, 23.8, 23.8],
        'IDSW': [2580, 1686, 2241],
        'FPS':  [6.5, 18.5, 43.5]
    },
    "MOT17": {
        'Tracker': ['StrongSORT', 'DeepOCSORT', 'ByteTrack'],
        'HOTA': [42.8, 40.4, 39.7],
        'IDF1': [51.3, 47.6, 46.9],
        'DetA': [35.4, 34.1, 34.8],
        'AssA': [52.0, 48.1, 45.6],
        'IDSW': [2943, 2355, 2949],
        'FPS':  [14.5, 22.0, 28.0]
    },
    "MOT20": {
        'Tracker': ['StrongSORT', 'DeepOCSORT', 'ByteTrack'],
        'HOTA': [14.5, 14.0, 14.3],
        'IDF1': [14.7, 13.7, 14.7],
        'DetA': [7.8, 7.0, 7.9],
        'AssA': [27.0, 27.9, 25.9],
        'IDSW': [2001, 1369, 1964],
        'FPS':  [5.0, 8.5, 11.0]
    }
}

# --- 2. ADVANCED CSS (Dark Glassmorphism) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Global Theme */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(at 0% 0%, rgba(16, 23, 42, 1) 0, transparent 50%), 
                          radial-gradient(at 100% 0%, rgba(15, 23, 42, 1) 0, transparent 50%);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    h1 {
        background: linear-gradient(to right, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1E293B;
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #60A5FA;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricValue"] {
        color: #60A5FA !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #60A5FA !important;
        border-bottom-color: #60A5FA !important;
    }
    
    /* Footer */
    .footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #020617; color: #64748B;
        text-align: center; padding: 12px;
        border-top: 1px solid #1E293B; font-size: 0.85rem;
        z-index: 999;
    }
    .footer a { color: #60A5FA; text-decoration: none; }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5);
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER: Image Loader ---
def show_asset(filename, caption):
    path = os.path.join(ASSET_DIR, filename)
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.warning(f"Image placeholder: {filename}")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("👁️ RobustMOT")
    st.caption("Thesis Dashboard v2.0")
    
    nav = st.radio("Navigate:", 
        ["1. Abstract & Overview", 
         "2. Methodology", 
         "3. Visual Analysis", 
         "4. Benchmarks (3 Datasets)", 
         "5. Conclusion"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎓 Thesis Details")
    st.markdown("**Supervisor:**\nDr. Md. Abdul Awal")
    st.markdown("**Institution:**\nIUBAT, Bangladesh")
    st.success("**Authors:**\nShah Mohammad Rizvi\nRume Akter")
    
    st.markdown("---")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Code-white?logo=github)](https://github.com/smri29/RobustMOTOcclusion)")

# --- 4. PAGE LOGIC ---

# PAGE 1: OVERVIEW
if nav == "1. Abstract & Overview":
    st.markdown("# Robust Multi-Object Tracking Under Heavy Occlusion")
    st.markdown("### A Comparative Analysis of DeepOCSORT, StrongSORT, and ByteTrack")
    
    col_ab, col_vis = st.columns([1.5, 1])
    
    with col_ab:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 Abstract")
        st.write("""
        Tracking objects in chaotic environments is a critical challenge in computer vision. 
        Standard algorithms fail when targets undergo **non-linear motion** (e.g., dancing) or **heavy occlusion** (e.g., crowds).
        
        This thesis presents a comprehensive benchmark of three SOTA trackers across **three datasets** (DanceTrack, MOT17, MOT20).
        We demonstrate that **DeepOCSORT** provides the optimal balance of stability and efficiency.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # High Level Metrics
        k1, k2, k3 = st.columns(3)
        k1.metric("Datasets Tested", "3", "Dance, Street, Crowd")
        k2.metric("Stability Gain", "+35%", "vs Baseline")
        k3.metric("Inference Speed", "18.5 FPS", "Real-Time Capable")

    with col_vis:
        show_asset("Figure_5_Qualitative_Filmstrip.png", "Fig 1: DeepOCSORT maintaining identity through occlusion.")

# PAGE 2: METHODOLOGY
elif nav == "2. Methodology":
    st.markdown("## 🔬 Methodology & Architecture")
    
    tab1, tab2 = st.tabs(["Pipeline", "Equations"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🛠️ Experimental Setup")
            st.markdown("""
            * **Detection:** YOLOv8x (Conf: 0.3)
            * **Tracking:** BoxMOT Framework
            * **Hardware:** NVIDIA A100-SXM4 (40GB)
            * **Datasets:**
                1. **DanceTrack:** Non-linear motion & uniforms.
                2. **MOT17:** Standard street surveillance.
                3. **MOT20:** Extreme crowd density.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            show_asset("Figure_15_Methodology_Pipeline.png", "Fig 2: The Comparative Tracking Pipeline")

    with tab2:
        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.info("**HOTA (Higher Order Tracking Accuracy)**")
            st.latex(r'''HOTA = \sqrt{DetA \cdot AssA}''')
            st.write("Balances Detection (finding the box) and Association (keeping the ID).")
        with col_eq2:
            st.info("**IDF1 (ID F1 Score)**")
            st.latex(r'''IDF1 = \frac{2IDTP}{2IDTP + IDFP + IDFN}''')
            st.write("Measures tracking stability. High IDF1 means fewer ID switches.")

# PAGE 3: VISUAL ANALYSIS
elif nav == "3. Visual Analysis":
    st.markdown("## 🎥 Visual Qualitative Analysis")
    st.write("Explore how the trackers perform across different datasets.")

    # Select Dataset
    dataset_choice = st.selectbox("Select Dataset:", list(VIDEO_DB.keys()))
    
    # Select Tracker
    tracker_choice = st.selectbox("Select Tracker:", list(VIDEO_DB[dataset_choice].keys()))

    # Select Video
    video_choice = st.selectbox("Select Sequence:", list(VIDEO_DB[dataset_choice][tracker_choice].keys()))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_url = VIDEO_DB[dataset_choice][tracker_choice][video_choice]
        if "placeholder" in video_url:
             st.warning("Video not available yet.")
        else:
             st.video(video_url)
             st.caption(f"{video_choice} | Tracker: {tracker_choice}")

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Analysis")
        st.write("Observe the tracking consistency and identity retention.")
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 4: BENCHMARKS
elif nav == "4. Benchmarks (3 Datasets)":
    st.markdown("## 📊 Comprehensive Results")
    
    # Dataset Selector for Data
    target_ds = st.radio("Select Benchmark Dataset:", ["DanceTrack", "MOT17", "MOT20"], horizontal=True)
    df_curr = pd.DataFrame(data_dict[target_ds])
    
    # Row 1: Charts
    col_bar, col_radar = st.columns([1.5, 1])
    
    with col_bar:
        st.markdown(f"### {target_ds} Performance")
        fig = px.bar(df_curr, x='Tracker', y=['HOTA', 'DetA', 'AssA'], barmode='group',
                     color_discrete_sequence=['#ff0055', '#00d2ff', '#00ffaa'], template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_radar:
        st.markdown("### Holistic Profile")
        categories = ['HOTA', 'IDF1', 'DetA', 'AssA']
        fig_radar = go.Figure()
        colors = ['#ff0055', '#00d2ff', '#00ffaa']
        
        for i, t in enumerate(df_curr['Tracker']):
            vals = df_curr.loc[df_curr['Tracker'] == t, categories].values.flatten().tolist()
            vals += vals[:1]
            fig_radar.add_trace(go.Scatterpolar(r=vals, theta=categories+[categories[0]], fill='toself', name=t, line_color=colors[i]))
            
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 70])), 
                                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="white"), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

    # Row 2: Deep Dive Figures
    st.markdown("### 📉 Stability & Error Analysis")
    col_err, col_seq = st.columns(2)
    with col_err:
        show_asset("Figure_9_Error_Donut.png", "Error Distribution (Log Scale)")
    with col_seq:
        # Check if 7 exists, otherwise show 12 or others
        if os.path.exists(os.path.join(ASSET_DIR, "Figure_7_ID_Switches.png")):
             show_asset("Figure_7_ID_Switches.png", "ID Switches Comparison")
        else:
             show_asset("Figure_12_Efficiency_Frontier.png", "Efficiency Analysis")


# PAGE 5: CONCLUSION
elif nav == "5. Conclusion":
    st.markdown("# 🏆 Final Verdict & Global Benchmark")
    
    # 1. VISUAL VERDICT CARDS
    col_winner, col_runner, col_speed = st.columns(3)
    
    with col_winner:
        st.markdown('<div class="glass-card" style="border-top: 4px solid #F43F5E;">', unsafe_allow_html=True)
        st.markdown("### 🥇 Accuracy King")
        st.markdown("## StrongSORT")
        st.write("Best for **Offline Processing**.")
        st.caption("Dominated DanceTrack & MOT17 in HOTA scores. Best identity preservation (ReID).")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_runner:
        st.markdown('<div class="glass-card" style="border-top: 4px solid #3B82F6;">', unsafe_allow_html=True)
        st.markdown("### 🥈 The Balanced Choice")
        st.markdown("## DeepOCSORT")
        st.write("Best for **Real-Time Apps**.")
        st.caption("Only ~2% accuracy drop vs StrongSORT but **3x Faster**. Best ID Stability.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_speed:
        st.markdown('<div class="glass-card" style="border-top: 4px solid #10B981;">', unsafe_allow_html=True)
        st.markdown("### ⚡ Speed Demon")
        st.markdown("## ByteTrack")
        st.write("Best for **Embedded Devices**.")
        st.caption("Incredibly fast (40+ FPS) but fails catastrophically in heavy occlusion.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # 2. THE GRANDMASTER TABLE
    st.markdown("### 📊 The Grandmaster Comparison Table")
    st.write("Side-by-side performance metrics across all three datasets.")
    
    # Constructing the Mega Dataframe
    # We want rows to be Trackers, Columns to be metrics per dataset
    
    df_mega = pd.DataFrame({
        "Tracker": ["StrongSORT", "DeepOCSORT", "ByteTrack"],
        "Dance HOTA": [42.2, 39.4, 38.2],
        "MOT17 HOTA": [42.8, 40.4, 39.7],
        "MOT20 HOTA": [14.5, 14.0, 14.3],
        "Dance IDF1": [40.4, 37.2, 39.5],
        "Avg FPS": [6.5, 18.5, 43.5],
        "Avg IDSW": [2508, 1803, 2384] # Approx averages
    })
    
    # Configuring the Styled Dataframe
    st.dataframe(
        df_mega,
        column_config={
            "Tracker": st.column_config.TextColumn("Algorithm", width="medium"),
            "Dance HOTA": st.column_config.ProgressColumn("DanceTrack HOTA", format="%.1f%%", min_value=0, max_value=50),
            "MOT17 HOTA": st.column_config.ProgressColumn("MOT17 HOTA", format="%.1f%%", min_value=0, max_value=50),
            "MOT20 HOTA": st.column_config.ProgressColumn("MOT20 HOTA", format="%.1f%%", min_value=0, max_value=20),
            "Dance IDF1": st.column_config.NumberColumn("Dance IDF1", format="%.1f"),
            "Avg FPS": st.column_config.NumberColumn("Speed (FPS)", format="%.1f ⚡"),
            "Avg IDSW": st.column_config.NumberColumn("ID Switches", format="%d 📉"),
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("---")
    
    # 3. FINAL RECOMMENDATION
    col_rec_img, col_rec_txt = st.columns([1, 2])
    
    with col_rec_img:
        show_asset("Figure_4_Speed_vs_Accuracy.png", "Efficiency Frontier") # Or 12 if 4 missing
        
    with col_rec_txt:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Thesis Recommendation")
        st.info("""
        Based on the comparative analysis of 25 DanceTrack sequences, 7 MOT17 sequences, and 4 MOT20 sequences:
        
        **We recommend DeepOCSORT for general-purpose deployment.**
        
        While StrongSORT offers marginally better accuracy (HOTA +2.8%), the computational cost is too high for live applications. 
        DeepOCSORT provides the critical "sweet spot" — robust enough to handle the dance occlusions, fast enough to run live.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>Developed by <a href="https://www.linkedin.com/in/smri29/" target="_blank">Shah Mohammad Rizvi</a> | IUBAT B.Sc. Thesis 2025</p>
</div>
""", unsafe_allow_html=True)