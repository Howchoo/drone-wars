# drone-wars
The Dunning-Kruger Experience's working repository for the [OpenWERX](http://www.sofwerx.org/openwerx/) drone competition. (reset Zach's wifi)

## Dependencies
### Software
* Python 2.7
* [TkInter](https://wiki.python.org/moin/TkInter)
* Aircrack-ng 1.2 RC 4 (https://www.aircrack-ng.org/)
* iwconfig
* xterm
* iw
* VNC server and client (optional)

### Hardware
* Wireless device with monitor mode capability
* HackRF (required for some functionality)

## Running DDrone GUI
1. Clone and navigate to this repository.
2. Run `sudo python ddrone/gui.py` (must be run as sudo)

## Running DDrone GUI on Remote Computer (e.g. Raspberry Pi)
This program is capable of being run on a Raspberry Pi mounted to a separate (non-target) drone. To do this, you'll want to [install a VNC server on your Raspberry Pi](https://howchoo.com/g/yzm1nmq5ngq/how-to-setup-vnc-on-your-raspberry-pi) to access the DDrone GUI from a remote machine.

## Disclaimer
Do not use this software for illegal purposes. It was developed for and is being provided as part of a research project. Signal spoofing and/or jamming is illegal in most countries -- don't do illegal things.

## License (GNU GPL)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
