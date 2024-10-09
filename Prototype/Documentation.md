# DSP prototype

## Requirements
The following requirements must be met.
1. First do:
```cmd
sudo apt update
sudo apt install build-essential libasound2-dev
git clone https://github.com/librespot-org/librespot.git
cd librespot
cargo build --release
./target/release/librespot --name "MyPi"
```
for the spotify librespot client.

2. Then install looback device:
```cmd
sudo apt install pulseaudio pavucontrol
```

3. Then install pyaudio to capture theaudio data from the virtual device:
```cmd
sudo apt install python3-pyaudio
pip3 install pyaudio
```

4. For doing real-time fft, we utilize the GPU and theGPU_FFT library on the pi.
```cmd
cd /opt/vc/src/hello_pi/hello_fft
make
sudo mknod char_dev c 100 0
```

5. Matplotlib and numpy for plotting and debugging the dsp:
```cmd
sudo apt install python3-matplotlib python3-numpy
```

6. Then set up the virtual loopback device:
```cmd
pactl load-module module-null-sink sink_name=loopback
pactl load-module module-loopback sink=loopback
```

That should be all the requirements.