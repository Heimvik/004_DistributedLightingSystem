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
    git

# Install Rust and Cargo (Rust package manager)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Clone librespot repository and build it
git clone https://github.com/librespot-org/librespot.git
cd librespot
cargo build --release
cd ..

# Setup GPU_FFT
cd /opt/vc/src/hello_pi/hello_fft
make
sudo mknod char_dev c 100 0

# Install Python libraries from requirements.txt
pip3 install -r requirements.txt

# Set up virtual loopback device
pactl load-module module-null-sink sink_name=loopback
pactl load-module module-loopback sink=loopback

echo "Setup completed!"