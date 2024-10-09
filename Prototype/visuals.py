import time
#from rpi_ws281x import PixelStrip, Color
import json
import threading

VISUALS_CONFIG_PATH = "visualsConfig.json"
LED_FREQ_HZ = 800000  
LED_DMA = 10         
LED_INVERT = False    
LED_CHANNEL = 0       

def loadBarConfig(filePath):
    try:
        with open(filePath, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The file '{filePath}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file '{filePath}' is not a valid JSON.")
        return {}

def initBars():
    config = loadBarConfig(VISUALS_CONFIG_PATH);
    print(config)

def runBars():
    initBars()

def runVisualsThread():
    visualsThread = threading.Thread(target=runBars)
    visualsThread.start()
    return visualsThread
