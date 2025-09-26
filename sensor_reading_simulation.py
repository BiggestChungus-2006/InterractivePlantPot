import random
import time

def read_simulated_sensors():
    """
    Generates a dictionary of fake sensor data with random values.
    This is used for testing the application without any physical hardware.

    Returns:
        A dictionary with simulated sensor data.
    """
    # Generate random values within a realistic range for each sensor
    data = {
        "soil": random.randint(10, 99),   # % moisture
        "light": random.randint(10, 99),  # % light level
        "temp": random.randint(15, 35)    # degrees Celsius
    }
    
    print(f"(SIMULATOR): Generated data: {data}")
    return data

# --- STANDALONE TEST BLOCK ---
# If you run this file directly (python sensor_simulator.py), it will generate data.
if __name__ == "__main__":
    print("\n--- Starting Standalone Simulator Test ---")
    print("Generating new simulated data every 100 seconds. Press Ctrl+C to stop.")
    while True:
        read_simulated_sensors()
        time.sleep(100)
        #Has been tested for every 5, 60 and 25 seconds and some extra values 