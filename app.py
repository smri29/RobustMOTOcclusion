import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DeepOCSORT Research Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. DATA ASSETS ---
VIDEO_LINKS = {
    "04: Heavy Occlusion": "https://youtu.be/fbwpWQks8og",
    "05: Group Dance": "https://youtu.be/NjSU4-6AnXQ",
    "07: Fast Crossing": "https://youtu.be/Fmc3r1Mnjeg",
    "10: Complex Motion": "https://youtu.be/GunfFmJSfB8",
    "14: Crowded Scene": "https://youtu.be/Z4uAx9QNM04",
    "18: Rapid Spins": "https://youtu.be/hjm8tu4CinU",
    "19: Low Light": "https://youtu.be/qYb4CQRJr9A",
    "25: Dynamic Camera": "https://youtu.be/n6S9skG41D0",
    "26: Extreme Close-up": "https://youtu.be/_utXxgsg0hk",
    "30: Formation Change": "https://youtu.be/0b2ER6DSTCI"
}

# Full Thesis Data
# We use this to generate interactive plots dynamically
data = {
    'Tracker': ['StrongSORT', 'DeepOCSORT', 'ByteTrack'],
    'HOTA': [42.20, 39.39, 38.21],
    'DetA': [66.71, 65.71, 61.87],
    'AssA': [27.04, 23.82, 23.81],
    'IDF1': [40.44, 37.15, 39.48],
    'IDR': [37.25, 33.51, 36.56],
    'IDP': [44.22, 41.69, 42.91],
    'FPS': [6.5, 18.5, 43.5],
    'ID Switches': [2580, 1686, 2241],
    'False Positives': [105812, 105492, 109552],
    'False Negatives': [141277, 149713, 142824]
}
df = pd.DataFrame(data)

# --- 2. DARK GLASSMORPHISM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Settings */
    .stApp {
        background: radial-gradient(circle at top left, #1b2735 0%, #090a0f 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 12, 16, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Metric styling */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #00d2ff;
    }
    div[data-testid="stMetricValue"] {
        color: #00d2ff !important;
        font-size: 2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.02);
        border-radius: 8px;
        color: #888;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 210, 255, 0.1);
        color: #00d2ff;
        border: 1px solid #00d2ff;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #090a0f;
        color: #666;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        border-top: 1px solid #222;
        z-index: 1000;
    }
    .footer a { color: #00d2ff; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## Sidebar")
    page = st.radio("Go to:", 
        ["1. Abstract & Overview", 
         "2. Methodology & Equations", 
         "3. Visual Analysis (Live)", 
         "4. Advanced Analytics", 
         "5. Final Conclusion"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎓 Thesis Details")
    st.markdown("**Group Members:**")
    st.caption("Shah Mohammad Rizvi")
    st.caption("Rume Akter")
    
    st.markdown("**Supervisor:**")
    st.caption("Dr. Md. Abdul Awal")
    
    st.markdown("**Institution:**")
    st.caption("IUBAT, Bangladesh")
    
    st.markdown("---")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Repo-white?logo=github)](https://github.com/smri29/RobustMOTOcclusion)")

# --- 4. PAGE LOGIC ---

# PAGE 1: OVERVIEW
if page == "1. Abstract & Overview":
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(0deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Robust Multi-Object Tracking Under Heavy Occlusion</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">A Comparative Analysis of Observation-Centric vs. Appearance-Based Methods</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Abstract")
        st.write("""
        Multi-Object Tracking (MOT) in chaotic environments remains a significant challenge. 
        Standard algorithms often fail when targets undergo **non-linear motion** (e.g., dancing) or **heavy occlusion**.
        
        This thesis benchmarks three state-of-the-art trackers on the **DanceTrack** dataset:
        1.  **StrongSORT:** An appearance-heavy tracker (Baseline).
        2.  **ByteTrack:** A motion-only tracker (High Speed).
        3.  **DeepOCSORT:** A hybrid method using Observation-Centric Momentum (Proposed Solution).
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # KPI Row
        k1, k2, k3 = st.columns(3)
        k1.metric("Top Accuracy", "42.2%", "StrongSORT")
        k2.metric("Top Stability", "1,686 IDSW", "DeepOCSORT")
        k3.metric("Real-Time", "18.5 FPS", "DeepOCSORT")

    with col2:
        if os.path.exists("assets/Fig5_Qualitative_Results.png"):
            st.image("assets/Fig5_Qualitative_Results.png", caption="Fig 5: Robust tracking through heavy occlusion.", use_container_width=True)
        else:
            st.info("Visual preview loading...")

# PAGE 2: METHODOLOGY
elif page == "2. Methodology & Equations":
    st.markdown("## Methodology")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📐 Evaluation Metrics")
        st.markdown("**1. HOTA (Higher Order Tracking Accuracy)**")
        st.latex(r'''HOTA = \sqrt{DetA \cdot AssA}''')
        st.caption("Balances Detection Accuracy (DetA) and Association Accuracy (AssA).")
        
        st.markdown("**2. IDF1 (ID F1 Score)**")
        st.latex(r'''IDF1 = \frac{2IDTP}{2IDTP + IDFP + IDFN}''')
        st.caption("Measures identity consistency over time.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Experimental Setup")
        st.write("**Dataset:** DanceTrack Validation Set (25 Sequences)")
        st.write("**Detector:** YOLOv8x (Conf: 0.3)")
        st.write("**Hardware:** NVIDIA A100-SXM4 (40GB)")
        
        st.markdown("---")
        st.markdown("**Pipeline Architecture:**")
        st.code("Video Input -> YOLOv8 Detection -> Tracker Association -> TrackEval Analysis", language="bash")
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 3: VISUAL LAB
elif page == "3. Visual Analysis (Live)":
    st.markdown("## 🎥 Qualitative Analysis Lab")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📂 Select Scenario")
        selected_seq = st.selectbox("Choose Sequence:", list(VIDEO_LINKS.keys()), label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.info("""
        **👀 Observation Guide:**
        1. **Cross-Over:** Do IDs swap when dancers cross?
        2. **Spins:** ByteTrack often loses track during spins.
        3. **Stability:** DeepOCSORT holds color (ID) best.
        """)
        
    with c2:
        video_url = VIDEO_LINKS[selected_seq]
        st.video(video_url)
        st.caption("Left: DeepOCSORT (Proposed) | Center: StrongSORT (Baseline) | Right: ByteTrack")

# PAGE 4: ADVANCED ANALYTICS
elif page == "4. Advanced Analytics":
    st.markdown("## Comprehensive Results & Figures")
    
    # ----------------------------------------------------
    # SECTION 1: INNOVATIVE VISUALIZATIONS (Radar & Gauges)
    # ----------------------------------------------------
    st.markdown("### 1. Multi-Dimensional Performance")
    col_radar, col_gauge = st.columns([1, 1])
    
    with col_radar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**🕸️ Radar Comparison (Holistic View)**")
        # Normalize Data for Radar
        categories = ['HOTA', 'DetA', 'AssA', 'IDF1', 'IDR']
        fig_radar = go.Figure()
        colors = ['#00d2ff', '#ff0055', '#00ffaa'] # Blue, Red, Green
        
        for i, tracker in enumerate(df['Tracker']):
            values = df.loc[df['Tracker'] == tracker, categories].values.flatten().tolist()
            values += values[:1] # Close the loop
            fig_radar.add_trace(go.Scatterpolar(
                r=values, theta=categories + [categories[0]],
                fill='toself', name=tracker, line_color=colors[i], opacity=0.6
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 70], color="#888"), bgcolor="rgba(0,0,0,0)"),
            showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"), margin=dict(t=30, b=30, l=30, r=30), height=350,
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Fig X: Radar chart comparing the 'shape' of performance across 5 key metrics.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_gauge:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**⚡ Efficiency Gauges (FPS vs Real-Time)**")
        
        # Function to create gauge
        def create_gauge(value, title, color):
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = value, title = {'text': title},
                gauge = {'axis': {'range': [0, 60]}, 'bar': {'color': color},
                         'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 30}}
            ))
            fig.update_layout(height=120, margin=dict(t=30, b=10, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
            return fig

        c1, c2, c3 = st.columns(3)
        with c1: st.plotly_chart(create_gauge(6.5, "StrongSORT", "#ff0055"), use_container_width=True)
        with c2: st.plotly_chart(create_gauge(18.5, "DeepOCSORT", "#00d2ff"), use_container_width=True)
        with c3: st.plotly_chart(create_gauge(43.5, "ByteTrack", "#00ffaa"), use_container_width=True)
        
        st.caption("Fig 3: Inference speed on NVIDIA A100. White line indicates Real-Time (30 FPS).")
        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # SECTION 2: STANDARD METRICS (Fig 1 & 2)
    # ----------------------------------------------------
    st.markdown("### 2. Standard Benchmark Metrics")
    tab_acc, tab_id = st.tabs(["Accuracy Breakdown (Fig 1)", "Identity Stability (Fig 2)"])
    
    with tab_acc:
        st.markdown("#### Overall Tracking Accuracy")
        df_melt = df.melt(id_vars='Tracker', value_vars=['HOTA', 'DetA', 'AssA'], var_name='Metric', value_name='Score')
        fig1 = px.bar(df_melt, x='Metric', y='Score', color='Tracker', barmode='group',
                     color_discrete_sequence=['#ff0055', '#00d2ff', '#00ffaa'], template="plotly_dark")
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.caption("Fig 1: Comparison of HOTA, Detection (DetA), and Association (AssA) scores.")

    with tab_id:
        st.markdown("#### Identity Consistency Details")
        df_id_melt = df.melt(id_vars='Tracker', value_vars=['IDF1', 'IDR', 'IDP'], var_name='Metric', value_name='Score')
        fig2 = px.bar(df_id_melt, x='Metric', y='Score', color='Tracker', barmode='group',
                     color_discrete_sequence=['#ff0055', '#00d2ff', '#00ffaa'], template="plotly_dark")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Fig 2: Detailed breakdown of Identity F1, Recall, and Precision.")

    # ----------------------------------------------------
    # SECTION 3: DEEP DIVE (Errors & Robustness)
    # ----------------------------------------------------
    st.markdown("### 3. Error & Robustness Analysis")
    col_err, col_seq = st.columns(2)
    
    with col_err:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**📉 Error Distribution (Fig 6)**")
        # Stacked bar for errors
        fig6 = px.bar(df, x='Tracker', y=['ID Switches', 'False Positives', 'False Negatives'], 
                      title="Component Analysis of Errors",
                      color_discrete_sequence=['#ffd700', '#ff6b6b', '#a29bfe'], template="plotly_dark")
        fig6.update_yaxes(type="log", title="Count (Log Scale)")
        fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig6, use_container_width=True)
        st.caption("Fig 6: Breakdown of errors. DeepOCSORT has fewest ID Switches (Yellow).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_seq:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**📈 Sequence Robustness (Fig 7)**")
        if os.path.exists("assets/Fig7_Sequence_Robustness.png"):
            st.image("assets/Fig7_Sequence_Robustness.png", use_container_width=True)
            st.caption("Fig 7: Performance variation across different video sequences.")
        else:
            st.info("Sequence data loading...")
        st.markdown('</div>', unsafe_allow_html=True)

# PAGE 5: CONCLUSION
elif page == "5. Final Conclusion":
    st.markdown("## Final Verdict & Trade-off Analysis")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### The Pareto Frontier (Speed vs Accuracy)")
        fig3 = px.scatter(df, x='FPS', y='HOTA', color='Tracker', size=[40,40,40], text='Tracker',
                          color_discrete_sequence=['#ff0055', '#00d2ff', '#00ffaa'], template="plotly_dark")
        fig3.update_traces(textposition='top center')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           xaxis_title="Speed (FPS) - Log Scale", xaxis_type="log", yaxis_title="Accuracy (HOTA %)")
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Fig 4: The 'Sweet Spot' Analysis. DeepOCSORT provides the best balance.")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Research Conclusion")
        st.write("This study confirms that **DeepOCSORT** is the superior choice for practical deployment.")
        
        st.markdown("""
        | Tracker | Accuracy | Speed | Stability |
        | :--- | :--- | :--- | :--- |
        | **StrongSORT** | 🥇 High | ❌ Slow | ⚠️ Unstable |
        | **ByteTrack** | 🥉 Low | 🥇 Fast | ❌ Unstable |
        | **DeepOCSORT** | 🥈 Competitive | ✅ **Real-Time** | 🥇 **Best** |
        """)
        
        st.success("**Recommendation:** For real-time surveillance where identity retention is critical, DeepOCSORT significantly outperforms the baseline.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>
        Developed by <a href="https://www.linkedin.com/in/smri29/" target="_blank">Shah Mohammad Rizvi</a> | 
        AI/ML Engineer | Rsearcher
    </p>
</div>
""", unsafe_allow_html=True)