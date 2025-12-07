import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

# Create assets folder if not exists
os.makedirs("assets", exist_ok=True)

# Data from Experiment
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
colors = ['#2e86de', '#e17055', '#00b894']

def generate_plots():
    print("📊 Generating Figures...")
    
    # Fig 1: Performance
    plt.figure(figsize=(10, 6))
    df_melted = df.melt(id_vars=['Tracker'], value_vars=['HOTA', 'DetA', 'AssA'], var_name='Metric', value_name='Score (%)')
    sns.barplot(x='Metric', y='Score (%)', hue='Tracker', data=df_melted, palette=colors)
    plt.savefig('assets/Fig1_Performance_Comparison.png', dpi=300)
    
    # Fig 4: Trade-off
    plt.figure(figsize=(9, 7))
    sns.scatterplot(data=df, x='FPS', y='HOTA', hue='Tracker', style='Tracker', s=400, palette=colors)
    plt.xscale('log')
    plt.savefig('assets/Fig4_Speed_vs_Accuracy.png', dpi=300)

    # Fig 6: Errors
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Tracker', y='ID Switches', data=df, palette=colors)
    plt.savefig('assets/Fig6_Error_Analysis.png', dpi=300)
    
    print("✅ Figures saved to 'assets/' folder.")

if __name__ == "__main__":
    generate_plots()