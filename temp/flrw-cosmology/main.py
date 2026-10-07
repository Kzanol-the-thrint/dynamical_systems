import csv
import config
from matrix import create_sdc_matrix
from sdc_solver import run_flrw_solver
from visualizer import render_plots

def save_flrw_trajectory_to_csv(trajectory, dt, output_csv):
    """Writes computed cosmological trajectory data from memory to CSV."""
    steps = len(trajectory)
    
    with open(output_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["step", "time_gyears", "scale_factor_a", "expansion_velocity_pa"])
        
        for i in range(steps):
            time_sec = i * dt
            time_gyears = time_sec / (365.25 * 86400.0 * 1e9)
            writer.writerow([i, time_gyears] + trajectory[i].tolist())
            
    print(f"Full FLRW trajectory written to '{output_csv}'.")

def main():
    # Load cosmological metrics from config/input
    cosmo_data = config.load_system_data()

    a_init = cosmo_data["a_init"]
    p_init = cosmo_data["p_init"]

    print("====================================================")
    print("Initializing FLRW Cosmological SDC Engine...")
    print(f"Forecast Horizon : {config.GIGA_YEARS} Giga-Years")
    print(f"Time Step (dt)   : {config.DT / (365.25 * 86400.0):.2f} Years")
    print(f"Density Params   : Omega_m={config.OMEGA_M0}, Omega_r={config.OMEGA_R0}, Omega_l={config.OMEGA_L0}")
    print("====================================================")

    # Build FLRW matrix operator
    matrix_map = create_sdc_matrix(
        config.OMEGA_M0, 
        config.OMEGA_R0, 
        config.OMEGA_L0, 
        config.H0, 
        config.DT
    )

    # Initial State Vector: [Scale Factor a, Expansion Momentum da/dt]
    initial_state = [a_init, p_init]

    # 1. Run FLRW numerical solver in RAM
    trajectory, steps = run_flrw_solver(
        matrix_map, 
        initial_state, 
        total_gy=config.GIGA_YEARS, 
        dt=config.DT
    )

    # 2. Render plots directly from memory
    render_plots(trajectory, config.DT, config.GIGA_YEARS)

    # 3. Export full trajectory to CSV
    save_flrw_trajectory_to_csv(trajectory, config.DT, config.OUTPUT_FILE)

    # 4. Terminal summary output
    a_init_val, a_final_val = trajectory[0, 0], trajectory[-1, 0]
    p_init_val, p_final_val = trajectory[0, 1], trajectory[-1, 1]

    print("\nCosmological simulation complete over", steps, "discrete steps.")
    print("----------------------------------------------------")
    print(f"Scale Factor a(t) : Initial = {a_init_val:.4f} | Final = {a_final_val:.4f}")
    print(f"Expansion Rate   : Initial = {p_init_val:.3e} | Final = {p_final_val:.3e}")
    print("----------------------------------------------------")

if __name__ == "__main__":
    main()