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

#Check for default device using
python3 -c "import sounddevice as sd; print(sd.query_devices())"

#Making two sinks combined:
heimvik@PLserver:~/Documents/004_DistributedLightingSystem/Prototype$ pactl list sinks
Sink #55
	State: SUSPENDED
	Name: alsa_output.platform-fef00700.hdmi.hdmi-stereo
	Description: Built-in Audio Digital Stereo (HDMI)
	Driver: PipeWire
	Sample Specification: s32le 2ch 48000Hz
	Channel Map: front-left,front-right
	Owner Module: 4294967295
	Mute: no
	Volume: front-left: 29490 /  45% / -20,81 dB,   front-right: 29490 /  45% / -20,81 dB
	        balance 0,00
	Base Volume: 65536 / 100% / 0,00 dB
	Monitor Source: alsa_output.platform-fef00700.hdmi.hdmi-stereo.monitor
	Latency: 0 usec, configured 0 usec
	Flags: HARDWARE DECIBEL_VOLUME LATENCY SET_FORMATS 
	Properties:
		alsa.card = "1"
		alsa.card_name = "vc4-hdmi-0"
		alsa.class = "generic"
		alsa.device = "0"
		alsa.driver_name = "vc4"
		alsa.id = "vc4hdmi0"
		alsa.long_card_name = "vc4-hdmi-0"
		alsa.name = "MAI PCM i2s-hifi-0"
		alsa.resolution_bits = "16"
		alsa.subclass = "generic-mix"
		alsa.subdevice = "0"
		alsa.subdevice_name = "subdevice #0"
		alsa.sync.id = "00000000:00000000:00000000:00000000"
		api.alsa.card.longname = "vc4-hdmi-0"
		api.alsa.card.name = "vc4-hdmi-0"
		api.alsa.path = "hdmi:1"
		api.alsa.pcm.card = "1"
		api.alsa.pcm.stream = "playback"
		audio.channels = "2"
		audio.position = "FL,FR"
		card.profile.device = "1"
		device.api = "alsa"
		device.class = "sound"
		device.id = "49"
		device.profile.description = "Digital Stereo (HDMI)"
		device.profile.name = "hdmi-stereo"
		device.routes = "1"
		factory.name = "api.alsa.pcm.sink"
		media.class = "Audio/Sink"
		device.description = "Built-in Audio"
		node.name = "alsa_output.platform-fef00700.hdmi.hdmi-stereo"
		node.nick = "MAI PCM i2s-hifi-0"
		node.pause-on-idle = "false"
		object.path = "alsa:acp:vc4hdmi0:1:playback"
		port.group = "playback"
		priority.driver = "1000"
		priority.session = "1000"
		factory.id = "19"
		clock.quantum-limit = "8192"
		client.id = "47"
		node.driver = "true"
		node.loop.name = "data-loop.0"
		library.name = "audioconvert/libspa-audioconvert"
		object.id = "55"
		object.serial = "55"
		api.acp.auto-port = "false"
		api.alsa.card = "1"
		api.alsa.use-acp = "true"
		api.dbus.ReserveDevice1 = "Audio1"
		api.dbus.ReserveDevice1.Priority = "-20"
		device.bus_path = "platform-fef00700.hdmi"
		device.enum.api = "udev"
		device.form_factor = "internal"
		device.icon_name = "audio-card-analog"
		device.name = "alsa_card.platform-fef00700.hdmi"
		device.nick = "vc4-hdmi-0"
		device.plugged.usec = "12604442"
		device.subsystem = "sound"
		sysfs.path = "/devices/platform/soc/fef00700.hdmi/sound/card1"
		device.string = "1"
	Ports:
		hdmi-output-0: HDMI / DisplayPort (type: HDMI, priority: 5900, availability group: Legacy 1, available)
	Active Port: hdmi-output-0
	Formats:
		pcm

Sink #59
	State: SUSPENDED
	Name: alsa_output.platform-fe00b840.mailbox.stereo-fallback
	Description: Built-in Audio Stereo
	Driver: PipeWire
	Sample Specification: s16le 2ch 48000Hz
	Channel Map: front-left,front-right
	Owner Module: 4294967295
	Mute: no
	Volume: front-left: 65536 / 100% / 0,00 dB,   front-right: 65536 / 100% / 0,00 dB
	        balance 0,00
	Base Volume: 56210 /  86% / -4,00 dB
	Monitor Source: alsa_output.platform-fe00b840.mailbox.stereo-fallback.monitor
	Latency: 0 usec, configured 0 usec
	Flags: HARDWARE HW_MUTE_CTRL HW_VOLUME_CTRL DECIBEL_VOLUME LATENCY 
	Properties:
		alsa.card = "0"
		alsa.card_name = "bcm2835 Headphones"
		alsa.class = "generic"
		alsa.device = "0"
		alsa.id = "Headphones"
		alsa.long_card_name = "bcm2835 Headphones"
		alsa.mixer_name = "Broadcom Mixer"
		alsa.name = "bcm2835 Headphones"
		alsa.resolution_bits = "16"
		alsa.subclass = "generic-mix"
		alsa.subdevice = "0"
		alsa.subdevice_name = "subdevice #0"
		alsa.sync.id = "00000000:00000000:00000000:00000000"
		api.alsa.card.longname = "bcm2835 Headphones"
		api.alsa.card.name = "bcm2835 Headphones"
		api.alsa.path = "hw:0"
		api.alsa.pcm.card = "0"
		api.alsa.pcm.stream = "playback"
		audio.channels = "2"
		audio.position = "FL,FR"
		card.profile.device = "1"
		device.api = "alsa"
		device.class = "sound"
		device.id = "48"
		device.profile.description = "Stereo"
		device.profile.name = "stereo-fallback"
		device.routes = "1"
		factory.name = "api.alsa.pcm.sink"
		media.class = "Audio/Sink"
		device.description = "Built-in Audio"
		node.name = "alsa_output.platform-fe00b840.mailbox.stereo-fallback"
		node.nick = "bcm2835 Headphones"
		node.pause-on-idle = "false"
		object.path = "alsa:acp:Headphones:1:playback"
		port.group = "playback"
		priority.driver = "1000"
		priority.session = "1000"
		factory.id = "19"
		clock.quantum-limit = "8192"
		client.id = "47"
		node.driver = "true"
		node.loop.name = "data-loop.0"
		library.name = "audioconvert/libspa-audioconvert"
		object.id = "54"
		object.serial = "59"
		api.acp.auto-port = "false"
		api.alsa.card = "0"
		api.alsa.use-acp = "true"
		api.dbus.ReserveDevice1 = "Audio0"
		api.dbus.ReserveDevice1.Priority = "-20"
		device.bus_path = "platform-fe00b840.mailbox"
		device.enum.api = "udev"
		device.form_factor = "internal"
		device.icon_name = "audio-card-analog"
		device.name = "alsa_card.platform-fe00b840.mailbox"
		device.nick = "bcm2835 Headphones"
		device.plugged.usec = "11792511"
		device.subsystem = "sound"
		sysfs.path = "/devices/platform/soc/fe00b840.mailbox/bcm2835-audio/sound/card0"
		device.string = "0"
	Ports:
		analog-output: Analog Output (type: Analog, priority: 9900, availability unknown)
	Active Port: analog-output
	Formats:
		pcm

Sink #250
	State: SUSPENDED
	Name: alsa_output.platform-snd_aloop.0.analog-stereo
	Description: Loopback Analog Stereo
	Driver: PipeWire
	Sample Specification: s32le 2ch 48000Hz
	Channel Map: front-left,front-right
	Owner Module: 4294967295
	Mute: no
	Volume: front-left: 58968 /  90% / -2,75 dB,   front-right: 58968 /  90% / -2,75 dB
	        balance 0,00
	Base Volume: 65536 / 100% / 0,00 dB
	Monitor Source: alsa_output.platform-snd_aloop.0.analog-stereo.monitor
	Latency: 0 usec, configured 0 usec
	Flags: HARDWARE HW_VOLUME_CTRL DECIBEL_VOLUME LATENCY 
	Properties:
		alsa.card = "3"
		alsa.card_name = "Loopback"
		alsa.class = "generic"
		alsa.device = "0"
		alsa.driver_name = "snd_aloop"
		alsa.id = "Loopback"
		alsa.long_card_name = "Loopback 1"
		alsa.mixer_name = "Loopback Mixer"
		alsa.name = "Loopback PCM"
		alsa.resolution_bits = "16"
		alsa.subclass = "generic-mix"
		alsa.subdevice = "0"
		alsa.subdevice_name = "subdevice #0"
		alsa.sync.id = "00000000:00000000:00000000:00000000"
		api.alsa.card.longname = "Loopback 1"
		api.alsa.card.name = "Loopback"
		api.alsa.path = "front:3"
		api.alsa.pcm.card = "3"
		api.alsa.pcm.stream = "playback"
		audio.channels = "2"
		audio.position = "FL,FR"
		card.profile.device = "11"
		device.api = "alsa"
		device.class = "sound"
		device.id = "94"
		device.profile.description = "Analog Stereo"
		device.profile.name = "analog-stereo"
		device.routes = "1"
		factory.name = "api.alsa.pcm.sink"
		media.class = "Audio/Sink"
		device.description = "Loopback"
		node.name = "alsa_output.platform-snd_aloop.0.analog-stereo"
		node.nick = "Loopback PCM"
		node.pause-on-idle = "false"
		object.path = "alsa:acp:Loopback:11:playback"
		port.group = "playback"
		priority.driver = "1009"
		priority.session = "1009"
		factory.id = "19"
		clock.quantum-limit = "8192"
		client.id = "47"
		node.driver = "true"
		node.loop.name = "data-loop.0"
		library.name = "audioconvert/libspa-audioconvert"
		object.id = "95"
		object.serial = "250"
		api.acp.auto-port = "false"
		api.alsa.card = "3"
		api.alsa.use-acp = "true"
		api.dbus.ReserveDevice1 = "Audio3"
		api.dbus.ReserveDevice1.Priority = "-20"
		device.bus_path = "platform-snd_aloop.0"
		device.enum.api = "udev"
		device.form_factor = "internal"
		device.icon_name = "audio-card-analog"
		device.name = "alsa_card.platform-snd_aloop.0"
		device.nick = "Loopback"
		device.plugged.usec = "4455366224"
		device.subsystem = "sound"
		sysfs.path = "/devices/platform/snd_aloop.0/sound/card3"
		device.string = "3"
	Ports:
		analog-output: Analog Output (type: Analog, priority: 9900, availability unknown)
	Active Port: analog-output
	Formats:
		pcm

pactl load-module module-null-sink sink_name=combined_sink sink_description="Combined Sink"

# Loopback from combined sink to the 3.5 mm aux
pactl load-module module-loopback source=combined_sink.monitor sink=alsa_output.platform-fe00b840.mailbox.stereo-fallback

# Loopback from combined sink to the loopback device
pactl load-module module-loopback source=combined_sink.monitor sink=alsa_output.platform-snd_aloop.0.analog-stereo

pactl set-default-sink combined_sink
