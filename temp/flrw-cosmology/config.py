import os
import csv

# FLRW Engine Execution Parameters
DT = 4.4e12           # Integration step size in seconds (~140,000 years per step, yielding ~100,000 total steps)
GIGA_YEARS = 14.0     # Forecast horizon in Giga-years
C_LIGHT = 2.99792458e8 
H0 = 2.2686e-18       # Hubble constant in s^-1
OMEGA_M0 = 0.315      
OMEGA_R0 = 9.0e-5     
OMEGA_L0 = 0.685      
INPUT_FILE = "input_cosmology.csv"
OUTPUT_FILE = "output_flrw_data.csv"

def load_system_data(csv_path=INPUT_FILE):
    if not os.path.exists(csv_path):
        return {
            "a_init": 0.1,     
            "p_init": 1.0e-10  
        }
        
    data = {}
    with open(csv_path, mode='r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row and len(row) >= 2:
                data[row[0].strip()] = float(row[1].strip())
    return data