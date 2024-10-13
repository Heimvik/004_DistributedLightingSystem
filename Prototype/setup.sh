#!/bin/bash

# Update and install system dependencies
sudo apt update
sudo apt install -y \
    build-essential \
    libasound2-dev \
    pulseaudio \
    pavucontrol \
    python3-pyaudio \
    python3-pip \
    python3-matplotlib \
    python3-numpy \
    curl \
    git \
    pkg-config

# Install Rust and Cargo (Rust package manager)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Clone librespot repository and build it
if [ ! -d "librespot" ]; then
    git clone https://github.com/librespot-org/librespot.git
else
    echo "librespot repository already exists."
fi

cd librespot
cargo build --release
cd ..

# Install Python libraries from requirements.txt
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Creating a new one."
    echo -e "pyaudio\nmatplotlib\nnumpy\nrpi_ws281x" > requirements.txt
    pip3 install -r requirements.txt
fi

# Set up virtual loopback device for capturing Spotify stream audio
echo "Setting up virtual loopback devices..."

# Ensure pulseaudio is running
pulseaudio --start

# Load loopback and null sink modules
pactl load-module module-null-sink sink_name=loopback || echo "Null sink already loaded"
pactl load-module module-loopback sink=loop
back || echo "Loopback module already loaded"

# Set default output to 3.5mm aux port
echo "Setting the Raspberry Pi's 3.5mm jack as default audio output..."
pactl set-default-sink 0  # On Raspberry Pi, sink 0 is typically the 3.5mm jack (HDMI is sink 1)

# Combine audio sinks: 3.5mm aux and loopback
echo "Combining the aux output and the loopback device for simultaneous audio routing..."
pactl load-module module-combine-sink sink_name=combined_output slaves=0,loopback

# Verify the available sinks
echo "Available sinks after setup:"
pactl list short sinks

echo "Setup completed successfully! Your Raspberry Pi will now output audio to both the 3.5mm jack and loopback for FFT processing."

#Forget the above, run this
sudo modprobe snd-aloop

#Check for loopback devices using 
aplay-l