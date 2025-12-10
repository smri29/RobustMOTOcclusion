import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

# Create assets folder if not exists
os.makedirs("assets", exist_ok=True)

# Data from Experiment (Updated with thesis results)
data = {
    'Tracker': ['StrongSORT', 'DeepOCSORT', 'ByteTrack'],
    'HOTA': [42.20, 39.39, 38.21],
    'DetA': [66.71, 65.71, 61.87],
    'AssA': [27.04, 23.82, 23.81],
    'IDF1': [40.44, 37.15, 39.48],
    'FPS': [6.5, 18.5, 43.5],
    'ID Switches': [2580, 1686, 2241]
}
df = pd.DataFrame(data)

# Style
sns.set_style("whitegrid")
# Colors: Blue for StrongSORT, Red/Orange for DeepOCSORT, Green for ByteTrack
colors = {'StrongSORT': '#2e86de', 'DeepOCSORT': '#e17055', 'ByteTrack': '#00b894'}

def generate_plots():
    print("📊 Generating Figures...")
    
    # Fig 1: Performance Comparison (Bar Chart)
    plt.figure(figsize=(10, 6))
    df_melted = df.melt(id_vars=['Tracker'], value_vars=['HOTA', 'DetA', 'AssA'], var_name='Metric', value_name='Score (%)')
    sns.barplot(x='Metric', y='Score (%)', hue='Tracker', data=df_melted, palette=colors)
    plt.title("Performance Comparison (HOTA, DetA, AssA)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig('assets/Fig1_Performance_Comparison.png', dpi=300)
    print("Saved Fig 1")
    
    # Fig 4: Trade-off (Scatter Plot)
    plt.figure(figsize=(9, 7))
    sns.scatterplot(data=df, x='FPS', y='HOTA', hue='Tracker', style='Tracker', s=400, palette=colors)
    plt.xscale('log')
    plt.title("Speed (FPS) vs Accuracy (HOTA)")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig('assets/Fig4_Speed_vs_Accuracy.png', dpi=300)
    print("Saved Fig 4")

    # Fig 6: Errors (Bar Chart for ID Switches)
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Tracker', y='ID Switches', data=df, palette=colors)
    plt.title("Identity Switches (Lower is Better)")
    plt.tight_layout()
    plt.savefig('assets/Fig6_Error_Analysis.png', dpi=300)
    print("Saved Fig 6")
    
    print("✅ All Figures saved to 'assets/' folder.")

if __name__ == "__main__":
    generate_plots()