# Distributed LED System

## Overview

The Distributed LED System is a networked lighting project using ESP32 microcontrollers and individually addressable RGB LED strips. The system consists of a master node that processes signals and multiple slave nodes, each controlling a 1-meter LED strip. The system supports various lighting modes, including synchronization with music and spatial sound effects.

## Features

- **Centralized Control**: Master node coordinates LED patterns across all slave nodes.
- **Dynamic Lighting Modes**:
  - Static Colors
  - Dynamic Patterns
  - Music Synchronization
  - Spatial Sound Effects
- **Real-time Communication**: Efficiently communicates between master and slave nodes using MQTT/WebSockets.
- **User Interface**: Web-based or mobile app interface for control and configuration.

## Components

- **ESP32 Development Boards** (for master and slave nodes)
- **1 Meter RGB LED Strips** (60 LEDs per meter)
- **Power Supplies** (suitable for the total power consumption of each node)
- **Connecting Cables** (for power and data connections)
- **Resistors and Capacitors** (for signal conditioning and stabilization)

## Installation

### Prerequisites

- **ESP32 Development Board**: Ensure you have the ESP32 boards installed in your Arduino IDE or PlatformIO.
- **MQTT Broker or WebSocket Server**: Set up a broker/server for communication (e.g., Mosquitto for MQTT, or a WebSocket server of your choice).

### Hardware Setup

1. **Connect LED Strips**:
   - Connect the data input of each LED strip to the corresponding GPIO pin on the ESP32.
   - Connect power and ground wires appropriately.

2. **Power Supply**:
   - Ensure each node has a stable power supply capable of handling the maximum power
