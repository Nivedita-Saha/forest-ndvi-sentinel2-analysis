import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("Generating seasonal NDVI time-series comparison...")

size = 1000

def generate_ndvi(season='summer', seed=42):
    np.random.seed(seed)
    if season == 'summer':
        base = 0.55
    else:  # spring — lower NDVI, snow melt
        base = 0.32

    ndvi = np.random.normal(base, 0.08, (size, size))

    # Dense forest patches
    for _ in range(12):
        cx, cy = np.random.randint(100, 900, 2)
        r = np.random.randint(60, 130)
        Y, X = np.ogrid[:size, :size]
        mask = (X - cx)**2 + (Y - cy)**2 <= r**2
        ndvi[mask] = np.random.normal(0.72 if season == 'summer' else 0.45, 0.05, mask.sum())

    # Clearcut areas
    for _ in range(6):
        cx, cy = np.random.randint(100, 900, 2)
        r = np.random.randint(30, 70)
        Y, X = np.ogrid[:size, :size]
        mask = (X - cx)**2 + (Y - cy)**2 <= r**2
        ndvi[mask] = np.random.normal(0.15 if season == 'summer' else 0.08, 0.06, mask.sum())

    # Lakes
    for _ in range(4):
        cx, cy = np.random.randint(100, 900, 2)
        rx, ry = np.random.randint(20, 60, 2)
        Y, X = np.ogrid[:size, :size]
        mask = ((X - cx)/rx)**2 + ((Y - cy)/ry)**2 <= 1
        ndvi[mask] = np.random.normal(-0.2, 0.05, mask.sum())

    return np.clip(ndvi, -1, 1)

# Generate both seasons
ndvi_spring = generate_ndvi('spring', seed=42)
ndvi_summer = generate_ndvi('summer', seed=42)
ndvi_diff = ndvi_summer - ndvi_spring

print(f"Spring NDVI Mean: {ndvi_spring.mean():.3f}")
print(f"Summer NDVI Mean: {ndvi_summer.mean():.3f}")
print(f"Mean NDVI Change: {ndvi_diff.mean():.3f}")

# --- Plot ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Spring
im1 = axes[0].imshow(ndvi_spring, cmap='RdYlGn', vmin=-0.3, vmax=0.85)
axes[0].set_title('Spring (April 2023)\nNDVI Mean: {:.3f}'.format(ndvi_spring.mean()), fontsize=12, fontweight='bold')
axes[0].set_xlabel('Pixel East (10m)')
axes[0].set_ylabel('Pixel North (10m)')
plt.colorbar(im1, ax=axes[0], label='NDVI', shrink=0.8)

# Summer
im2 = axes[1].imshow(ndvi_summer, cmap='RdYlGn', vmin=-0.3, vmax=0.85)
axes[1].set_title('Summer (July 2023)\nNDVI Mean: {:.3f}'.format(ndvi_summer.mean()), fontsize=12, fontweight='bold')
axes[1].set_xlabel('Pixel East (10m)')
plt.colorbar(im2, ax=axes[1], label='NDVI', shrink=0.8)

# Difference
im3 = axes[2].imshow(ndvi_diff, cmap='coolwarm_r', vmin=-0.4, vmax=0.4)
axes[2].set_title('Seasonal Change\n(Summer − Spring)', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Pixel East (10m)')
plt.colorbar(im3, ax=axes[2], label='NDVI Change', shrink=0.8)

fig.suptitle('Seasonal NDVI Comparison — Boreal Forest, Sweden (2023)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/ndvi_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/ndvi_timeseries.png")