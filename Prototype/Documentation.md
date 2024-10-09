# DSP prototype

## Server credentails
For the dsp server, the following credentials are used:
- username: heimvik
- ip: 192.168.0.134
Password is known.

## Requirements
The following is done in the setup.sh.
1. Running the requirements.

2.
. Configure curl
```cmd
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

3. First do:
```cmd
sudo apt update
sudo apt install build-essential libasound2-dev
git clone https://github.com/librespot-org/librespot.git
cd librespot
cargo build --release
./target/release/librespot --name "PLserver"
```
for the spotify librespot client.

4. Then install looback device:
```cmd
sudo apt install pulseaudio pavucontrol
```

5. Then install pyaudio to capture theaudio data from the virtual device:
```cmd
sudo apt install python3-pyaudio
pip3 install pyaudio
```

6. For doing real-time fft, we utilize the GPU and theGPU_FFT library on the pi.
```cmd
cd /opt/vc/src/hello_pi/hello_fft
make
sudo mknod char_dev c 100 0
```

7. Matplotlib and numpy for plotting and debugging the dsp:
```cmd
sudo apt install python3-matplotlib python3-numpy
```

8. Then set up the virtual loopback device:
```cmd
pactl load-module module-null-sink sink_name=loopback
pactl load-module module-loopback sink=loopback
```

That should be all the requirements.

Make sure the GUI is turned off, improving performance. Done by:
```cmd
sudo systemctl set-default multi-user.target
```