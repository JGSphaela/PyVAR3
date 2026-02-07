import time
import csv
import threading
import sys
import os
from datetime import datetime
from src.gpib.gpib_command_model335 import Model335GPIBCommand

# Flag to control the loop
keep_running = True

def input_listener():
    """Listens for 'q' + Enter to stop the script."""
    global keep_running
    print("Press 'q' and Enter to stop logging...")
    while keep_running:
        user_input = input()
        if user_input.strip().lower() == 'q':
            keep_running = False
            break

def log_temperature(duration=None, interval=1.0, channels=None, output_file=None):
    """
    Logs temperature from Model335.
    
    :param duration: Total time to run in seconds. If None, runs until 'q' is pressed.
    :param interval: Time in seconds between readings.
    :param channels: List of channels to log (e.g., ['A', 'B']). Defaults to ['A', 'B'].
    :param output_file: Output CSV filename. If None, generates one based on timestamp.
    """
    global keep_running
    
    if channels is None:
        channels = ['A', 'B']
    
    # Initialize instrument
    try:
        model_335 = Model335GPIBCommand()
        model_335.init_connection()
    except Exception as e:
        print(f"Error connecting to instrument: {e}")
        return

    # Generate filename if not provided
    if output_file is None:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"temperature_log_{timestamp_str}.csv"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)

    print(f"Logging channels {channels} to {output_file} every {interval} seconds.")
    
    # Prepare CSV headers
    headers = ['Timestamp', 'Time_Elapsed_s'] + [f'Temp_{ch} (K)' for ch in channels]
    
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        start_time = time.time()
        
        # Start input listener thread if no duration specified
        if duration is None:
            input_thread = threading.Thread(target=input_listener)
            input_thread.daemon = True
            input_thread.start()
        else:
            print(f"Running for {duration} seconds.")

        try:
            while keep_running:
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                # Check duration
                if duration is not None and elapsed_time >= duration:
                    print("Duration reached.")
                    break
                
                row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{elapsed_time:.2f}"]
                
                for ch in channels:
                    try:
                        temp = model_335.query_kelvin(input_channel=ch)
                        # Remove potential newlines or extra chars
                        temp = temp.strip()
                        row.append(temp)
                    except Exception as e:
                        print(f"Error reading channel {ch}: {e}")
                        row.append("Error")
                
                writer.writerow(row)
                csvfile.flush() # Ensure data is written
                print(f"Logged: {row}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nLogging stopped by KeyboardInterrupt.")
        finally:
            print(f"Logging finished. Data saved to {output_file}")

if __name__ == "__main__":
    # Example usage parsing
    # You can change these variables or use command line args in the future
    
    # Default settings
    log_duration = None # Set to valid number (seconds) for fixed time, or None for infinite
    log_interval = 1.0
    log_channels = ['A', 'B'] # Can be ['A'], ['B'], or ['A', 'B']
    
    # Simple CLI argument parsing could be added here, but for now we run with defaults
    # or prompt user.
    
    print("--- Temperature Logger ---")
    print("1. Log continuously (until 'q')")
    print("2. Log for fixed duration")
    choice = input("Select mode (1/2): ").strip()
    
    if choice == '2':
        try:
            log_duration = float(input("Enter duration in seconds: "))
        except ValueError:
            print("Invalid number, defaulting to continuous.")
            log_duration = None
            
    ch_input = input("Enter channels to log (A, B, or AB for both) [default AB]: ").strip().upper()
    if ch_input == 'A':
        log_channels = ['A']
    elif ch_input == 'B':
        log_channels = ['B']
    else:
        log_channels = ['A', 'B']
        
    log_temperature(duration=log_duration, interval=log_interval, channels=log_channels)
