"""
Generate a visualization for the thumbnail.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Create figure with specific size for thumbnail
fig, ax = plt.subplots(figsize=(12, 6.3), facecolor='#1a1a2e')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Add gradient-like background
from matplotlib.patches import Rectangle
colors = ['#667eea', '#764ba2', '#667eea']
for i, color in enumerate(colors):
    rect = Rectangle((0, i*3.33), 10, 3.33, facecolor=color, alpha=0.3)
    ax.add_patch(rect)

# Title
ax.text(5, 8.5, '📊 BI Intelligence Agent System', 
        fontsize=32, fontweight='bold', color='white',
        ha='center', va='center')

# Subtitle
ax.text(5, 7.5, 'Multi-Agent Business Intelligence Analyzer',
        fontsize=18, color='white', ha='center', va='center', alpha=0.9)

# Feature boxes
features = [
    ('🤖', '4 Specialized\nAgents', 1.5),
    ('⚡', '10x Faster\nAnalysis', 3.8),
    ('🧠', 'Continuous\nLearning', 6.1),
    ('📊', 'Professional\nReports', 8.4)
]

for emoji, text, x in features:
    # Box
    box = FancyBboxPatch((x-0.6, 4), 1.2, 1.8,
                          boxstyle="round,pad=0.1",
                          facecolor='#2d2d44',
                          edgecolor='#667eea',
                          linewidth=2,
                          alpha=0.8)
    ax.add_patch(box)
    
    # Emoji
    ax.text(x, 5.2, emoji, fontsize=28, ha='center', va='center')
    
    # Text
    ax.text(x, 4.5, text, fontsize=10, color='white',
            ha='center', va='center', multialignment='center')

# Agent architecture diagram (simplified)
agent_y = 2.5
agents = [
    ('Coordinator', 2, '#667eea'),
    ('Analyst', 4, '#764ba2'),
    ('Visualizer', 6, '#667eea'),
    ('Reporter', 8, '#764ba2')
]

for name, x, color in agents:
    circle = Circle((x, agent_y), 0.4, facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, agent_y-0.9, name, fontsize=9, color='white', ha='center', va='center')

# Arrows connecting agents
arrow_props = dict(arrowstyle='->', lw=2, color='white', alpha=0.5)
ax.annotate('', xy=(3.6, agent_y), xytext=(2.4, agent_y), arrowprops=arrow_props)
ax.annotate('', xy=(5.6, agent_y), xytext=(4.4, agent_y), arrowprops=arrow_props)
ax.annotate('', xy=(7.6, agent_y), xytext=(6.4, agent_y), arrowprops=arrow_props)

# Bottom text
ax.text(5, 0.8, 'Google AI Agents Intensive Course - Capstone Project',
        fontsize=12, color='white', ha='center', va='center', alpha=0.7)

ax.text(5, 0.3, 'Enterprise Agents Track | Powered by Gemini',
        fontsize=10, color='white', ha='center', va='center', alpha=0.6)

plt.tight_layout()
plt.savefig('/Users/c9c4dd/kaggle/thumbnail.png', dpi=100, bbox_inches='tight', 
            facecolor='#1a1a2e', edgecolor='none')
print("✅ Thumbnail created: thumbnail.png")
plt.close()

# Also create a simpler card image
fig, ax = plt.subplots(figsize=(8, 6), facecolor='#667eea')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Simple gradient background
from matplotlib.colors import LinearSegmentedColormap
gradient = np.linspace(0, 1, 100).reshape(1, -1)
gradient = np.vstack([gradient] * 100)
ax.imshow(gradient, extent=[0, 10, 0, 10], aspect='auto', 
          cmap=LinearSegmentedColormap.from_list('', ['#667eea', '#764ba2']))

# Main text
ax.text(5, 6.5, '📊', fontsize=80, ha='center', va='center')
ax.text(5, 4.5, 'BI Intelligence\nAgent System', 
        fontsize=28, fontweight='bold', color='white',
        ha='center', va='center', multialignment='center')
ax.text(5, 2.8, 'Multi-Agent Business Intelligence',
        fontsize=16, color='white', ha='center', va='center', alpha=0.9)
ax.text(5, 2.2, 'Google AI Agents Capstone',
        fontsize=14, color='white', ha='center', va='center', alpha=0.8)

plt.tight_layout()
plt.savefig('/Users/c9c4dd/kaggle/card_image.png', dpi=150, bbox_inches='tight',
            facecolor='#667eea', edgecolor='none')
print("✅ Card image created: card_image.png")
plt.close()

print("\n📸 Images created successfully!")
print("   - thumbnail.png (for main thumbnail)")
print("   - card_image.png (for card image)")
print("\nUpload these to your Kaggle submission!")

