import numpy as np

def create_sdc_matrix(omega_m, omega_r, omega_l, h0, dt):
    """
    Constructs the State-Dependent Coefficient (SDC) Matrix for FLRW Cosmology.
    State vector: [a, da/dt] or scale factor and expansion velocity dynamics.
    """
    # For a 2x2 or expanded canonical state representation [a, p_a]
    return np.array([
        # Row 0: Scale factor evolution (da/dt = momentum term)
        [lambda a, pa: 0.0, 
         lambda a, pa: 1.0],
         
        # Row 1: Friedmann acceleration equation mapped into SDC coefficient form
        [lambda a, pa: - (h0**2) * ((2.0 * omega_r / (a**5)) + (1.5 * omega_m / (a**4)) - omega_l),
         lambda a, pa: 0.0]
    ], dtype=object)