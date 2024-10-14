import time
from rpi_ws281x import PixelStrip, Color
import json

LED_FREQ = 800000
MA_SMOOTHING = 0.05
DMA_CHANNEL = 10
#PWM channels are only 0 and 1 avalibale on respectively GPIO 12 and 13

current_ma = {}

def load_led_bars_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config_list = json.load(file)
        
        # Check if the config is a list and contains objects with 'id'
        if not isinstance(config_list, list):
            raise ValueError("Config should be a list of LED bar configurations.")
        
        max_id = max(config['id'] for config in config_list)
        config_lst = [None] * (max_id + 1)  # Create a list of Nones with length equal to max_id + 1

        # Assign each configuration to the correct index in the list
        for config in config_list:
            config_lst[config['id']] = config
        
        return config_lst

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON.")
        return {}
    except KeyError:
        print("Error: One of the LED bar configurations is missing an 'id'.")
        return {}
    except ValueError as e:
        print(f"Error: {e}")
        return {}
    
def init_bars(config_lst):
    bars = []
    iter = 0
    print(config_lst)
    for config in config_lst:
        if config:  # Make sure config is not None (in case there are gaps in IDs)
            bars.append(PixelStrip(config['number_of_leds'], config['gpio'], LED_FREQ, DMA_CHANNEL, False, 255, config['pwm_channel']))
            bars[-1].begin()  # Begin for the latest added strip
    print("Bars initialized sucessfully!")
    return bars

def set_brightness_and_color(strip, brightness, color):
    strip.setBrightness(brightness)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(color[0], color[1], color[2]))
    strip.show()

'''
def visualize_beat(frequency, magnitudes, bar, color, sensitivity):

    Visualizes the beat at a given frequency by lighting up the LED strip if the magnitude at the frequency bin
    exceeds the moving average by a factor of 'sensitivity'.

    Args:
        frequency (float): The target frequency to detect the beat.
        magnitudes (list): The magnitudes of all frequency bins from the FFT.
        bar (PixelStrip): The LED strip object to visualize the beat.
        color (tuple): The RGB color to light up the strip (max brightness when beat detected).
        sensitivity (float): The factor to compare against the moving average (e.g., 1.5 for 50% increase).


    global current_ma

    # Find the index of the frequency bin closest to the target frequency
    freq_bin_index = find_nearest_bin(frequency, magnitudes)

    # Get the current magnitude of the nearest frequency bin
    current_magnitude = magnitudes[freq_bin_index]

    # If this frequency is not already tracked in the moving average, initialize it
    if frequency not in current_ma:
        current_ma[frequency] = current_magnitude  # Initialize with the current magnitude

    # Compare the current magnitude to the moving average, scaled by sensitivity
    if current_magnitude > sensitivity * current_ma[frequency]:
        # If the current magnitude exceeds the moving average, light up the LED strip
        for i in range(bar.numPixels()):
            bar.setPixelColor(i, Color(color[0], color[1], color[2]))  # Set to the max brightness
        bar.show()  # Display the changes

    # Update the moving average for this frequency (simple moving average)
    # You can choose a smoothing factor here (e.g., 0.1 means 10% new value, 90% old value)
    current_ma[frequency] = (1 - MA_SMOOTHING) * current_ma[frequency] + MA_SMOOTHING * current_magnitude
'''