import time
import rpi_ws281x
import json

def load_led_bars_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON.")
        return {}