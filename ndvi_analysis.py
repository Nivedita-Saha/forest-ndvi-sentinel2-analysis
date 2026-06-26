import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("Generating Swedish forest NDVI simulation...")

# --- Create realistic forest landscape (1000x1000 pixels at 10m = 10km x 10km) ---
size = 1000

# Base NDVI layer — boreal forest background
ndvi = np.random.normal(0.55, 0.08, (size, size))

# --- Add forest zones ---
# Dense conifer forest patches (high NDVI)
for _ in range(12):
    cx, cy = np.random.randint(100, 900, 2)
    r = np.random.randint(60, 130)
    Y, X = np.ogrid[:size, :size]
    mask = (X - cx)**2 + (Y - cy)**2 <= r**2
    ndvi[mask] = np.random.normal(0.72, 0.05, mask.sum())

# Clearcut / recently harvested areas (low NDVI)
for _ in range(6):
    cx, cy = np.random.randint(100, 900, 2)
    r = np.random.randint(30, 70)
    Y, X = np.ogrid[:size, :size]
    mask = (X - cx)**2 + (Y - cy)**2 <= r**2
    ndvi[mask] = np.random.normal(0.15, 0.06, mask.sum())

# Young regenerating forest (moderate NDVI)
for _ in range(8):
    cx, cy = np.random.randint(100, 900, 2)
    r = np.random.randint(40, 80)
    Y, X = np.ogrid[:size, :size]
    mask = (X - cx)**2 + (Y - cy)**2 <= r**2
    ndvi[mask] = np.random.normal(0.38, 0.07, mask.sum())

# Lakes / wetlands (negative NDVI)
for _ in range(4):
    cx, cy = np.random.randint(100, 900, 2)
    rx, ry = np.random.randint(20, 60, 2)
    Y, X = np.ogrid[:size, :size]
    mask = ((X - cx)/rx)**2 + ((Y - cy)/ry)**2 <= 1
    ndvi[mask] = np.random.normal(-0.2, 0.05, mask.sum())

# Roads / clearings (very low NDVI)
for _ in range(3):
    x1 = np.random.randint(0, size)
    ndvi[x1:x1+8, :] = np.random.normal(0.05, 0.02, (8, size))

# Clip to valid range
ndvi = np.clip(ndvi, -1, 1)

print(f"NDVI Min: {ndvi.min():.3f}, Max: {ndvi.max():.3f}, Mean: {ndvi.mean():.3f}")

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 10))
ndvi_plot = ax.imshow(ndvi, cmap='RdYlGn', vmin=-0.3, vmax=0.85)
cbar = plt.colorbar(ndvi_plot, ax=ax, label='NDVI Value', shrink=0.8)

ax.set_title('NDVI Forest Health Map — Boreal Forest, Sweden\n(Simulated from Sentinel-2 Band Statistics, July 2023)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Pixel East (10m resolution)')
ax.set_ylabel('Pixel North (10m resolution)')

# Scale bar
ax.plot([50, 150], [950, 950], 'k-', linewidth=3)
ax.text(100, 970, '1 km', ha='center', fontsize=9)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='darkgreen', label='Dense Conifer Forest (NDVI > 0.65)'),
    mpatches.Patch(facecolor='yellowgreen', label='Mixed/Regenerating Forest (0.35–0.65)'),
    mpatches.Patch(facecolor='yellow', label='Young Regrowth / Clearcut Edge (0.1–0.35)'),
    mpatches.Patch(facecolor='red', label='Harvested Area / Bare Ground (< 0.1)'),
    mpatches.Patch(facecolor='navy', label='Lakes / Wetlands (NDVI < 0)')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.9)

plt.tight_layout()
plt.savefig('outputs/ndvi_map.png', dpi=150)
plt.show()
print("Saved: outputs/ndvi_map.png")