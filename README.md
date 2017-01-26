# drone-wars
This repository is a collection of programs designed to exploit vulnerabilities in the DJI Phantom 3 and Phantom 4, as well as a GUI called DDrone that can be used to execute them.

Some hardware is required for certain exploits; we've listed this hardware below, and have opted to execute it on a Raspberry Pi, with all hardware mounted on a high-end hobbyist drone (the "attack drone").

This software was developed as a research project by the DKE (Dunning-Kruger Experience) group for the [OpenWERX](http://www.sofwerx.org/openwerx/) drone-hacking competition.

## Dependencies
### Software
* Python 2.7
* [TkInter](https://wiki.python.org/moin/TkInter)
* Aircrack-ng 1.2 RC 4 (https://www.aircrack-ng.org/)
* iwconfig
* xterm
* iw
* VNC server and client (optional, required for running DDrone on a remote device such as an attack drone)

### Hardware
* Wireless device with monitor mode capability
* HackRF One (required for some functionality)
* Alpha Packet Injection-Capable WiFi Dongle (Optional, required if your device doesn't support monitoring/packet injection)
* Raspberry Pi 3 (Optional, required for attack drone)
* Lithium Polymer battery (Optional, required for powering equipment on attack drone)
* Wiring harness for powering components (Optional, required for powering equipment on attack drone)

## DDrone GUI
The DDrone GUI allows you to execute programs using a graphical interface.

### Setup
1. Clone and navigate to this repository.
2. Run `sudo python ddrone/gui.py` (must be run as sudo)

### Running on aRemote Device (e.g. Raspberry Pi)
This program is capable of being run on a Raspberry Pi mounted to a separate (non-target) drone. To do this, you'll want to [install a VNC server on your Raspberry Pi](https://howchoo.com/g/yzm1nmq5ngq/how-to-setup-vnc-on-your-raspberry-pi) to access the DDrone GUI from a remote machine.

### Raspberry Pi VNC Setup
Format is `pi ip address`:`port number``desktop number`
```
[pi ip]:[port][desktop number]

[192.168.1.151]:[590][1]

192.168.1.151:5901
```
Default Raspberry Pi credentials:
```
user: pi
pass: raspberry
```

## DDrone Program Functionality based on by Phantom version (3/4)
Certain DDrone programs will only function on the Phantom 3 as the Phantom 3 has an open wireless connection. Additionally, some programs may no longer function as DJI closes vulnerabilities by releasing firmware updates.

### Phantom 3 Programs
All programs can currently be run on the Phantom 3.

### Phantom 4
Currently, only the GPS jamming/spoofing exploits can be performed on the Phantom 4.

## List of DDrone Programs
@todo

## Disclaimer
Do not use this software for illegal purposes. It was developed for and is being provided as part of a research project. Signal spoofing and/or jamming is illegal in most countries -- don't do illegal things.

## License (GNU GPL)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
