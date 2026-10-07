import matplotlib.pyplot as plt
import numpy as np

def render_plots(trajectory, dt, total_gy, output_dir="."):
    """
    Renders 3D Phase-Space Trajectory and 2D System Evolution plots for FLRW Cosmology as 
    perfect equal-sized squares fitting the portrait A4 layout.
    """
    steps = len(trajectory)
    # Convert time steps into Giga-years for readable axis scaling
    total_seconds_per_gy = 365.25 * 86400.0 * 1e9
    time_gyears = (np.arange(steps) * dt) / total_seconds_per_gy
    
    scale_factor = trajectory[:, 0]
    expansion_rate = trajectory[:, 1]
    
    # Select checkpoint indices (e.g., ~20 evenly spaced checkpoints along the horizon)
    checkpoint_count = min(20, steps)
    checkpoint_indices = np.linspace(0, steps - 1, checkpoint_count, dtype=int)

    # Perfect Square Dimensions: Equal width and height (~5.26 inches = 90% of half A4 height)
    square_size = (11.6929 * 0.5) * 0.9

    # 1. 3D Phase-Space Trajectory Rendering (Square)
    fig_ps = plt.figure(figsize=(square_size, square_size))
    ax_ps = fig_ps.add_subplot(111, projection='3d')
    
    ax_ps.plot(scale_factor, expansion_rate, time_gyears, color='#8e44ad', linewidth=1.2, label='FLRW Trajectory')
    ax_ps.scatter(scale_factor[checkpoint_indices], expansion_rate[checkpoint_indices], time_gyears[checkpoint_indices], 
                  color='#6c3483', s=20, label='Epoch Checkpoints', zorder=4)
    ax_ps.scatter([scale_factor[0]], [expansion_rate[0]], [time_gyears[0]], color='blue', s=40, label='Initial State', zorder=5)
    ax_ps.scatter([scale_factor[-1]], [expansion_rate[-1]], [time_gyears[-1]], color='black', s=40, label=f'Final ({total_gy:.1f} GY)', zorder=5)
    
    ax_ps.set_title(f"3D FLRW Phase-Space Manifold ({total_gy:.1f} GY)", fontsize=9, fontweight='bold')
    ax_ps.set_xlabel("Scale Factor $a(t)$", fontsize=8, labelpad=5)
    ax_ps.set_ylabel("Expansion Rate $\dot{a}(t)$", fontsize=8, labelpad=5)
    ax_ps.set_zlabel("Time (GY)", fontsize=8, labelpad=5)
    ax_ps.tick_params(axis='both', labelsize=7)
    ax_ps.legend(loc='upper left', fontsize=7)
    
    ps_file = f"{output_dir}/phase_space_trajectory.png"
    plt.tight_layout()
    plt.savefig(ps_file, dpi=300)
    plt.close(fig_ps)

    # 2. 2D System Evolution Subplots (Square)
    fig_2d, (ax1, ax2) = plt.subplots(2, 1, figsize=(square_size, square_size), sharex=True)
    
    ax1.plot(time_gyears, scale_factor, color='#2980b9', linewidth=1.4, label='Scale Factor $a(t)$')
    ax1.set_ylabel("Scale Factor ($a$)", fontsize=8, fontweight='bold')
    ax1.set_title(f"FLRW Scale Factor & Expansion History", fontsize=9, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.tick_params(axis='both', labelsize=7)
    ax1.legend(loc='upper left', fontsize=7)

    ax2.plot(time_gyears, expansion_rate, color='#c0392b', linewidth=1.4, label=r'Expansion Velocity $\dot{a}(t)$')
    ax2.set_xlabel("Cosmological Time (Giga-Years)", fontsize=8, fontweight='bold')
    ax2.set_ylabel(r"Expansion Rate ($\dot{a}$)", fontsize=8, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.tick_params(axis='both', labelsize=7)
    ax2.legend(loc='upper left', fontsize=7)

    ts_file = f"{output_dir}/system_evolution.png"
    plt.tight_layout()
    plt.savefig(ts_file, dpi=300)
    plt.close(fig_2d)
    print(f"Exported standardized FLRW square plots: {ps_file}, {ts_file}")