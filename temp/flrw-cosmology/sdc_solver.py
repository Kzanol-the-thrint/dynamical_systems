import numpy as np

def run_flrw_solver(matrix_map, initial_state, total_gy=14.0, dt=3.1536e7):
    total_seconds = total_gy * 1e9 * 365.25 * 86400.0
    steps = int(total_seconds / dt)
    Phi_state = np.array(initial_state, dtype=np.float64)
    
    trajectory = np.zeros((steps, 2), dtype=np.float64)

    for i in range(steps):
        a, pa = Phi_state
        
        # Prevent division by zero or collapse
        if a <= 1e-6:
            a = 1e-6
            
        A_num = np.zeros((2, 2), dtype=np.float64)
        for r in range(2):
            for c in range(2):
                A_num[r, c] = matrix_map[r, c](a, pa)
        
        # Symplectic/Euler SDC Step update
        Phi_next = Phi_state + np.dot(A_num, Phi_state) * dt
        Phi_state = Phi_next.copy()
        trajectory[i] = Phi_state.copy()

    return trajectory, steps