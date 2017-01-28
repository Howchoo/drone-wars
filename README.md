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

## Active DDrone Programs

### "Takeover" (Deauth) Program - Primary Attack Mechanism

#### Description:
Take over control of the drone by deauthenticating the pilot’s wireless device and connecting directly to the controller using our wireless device or a custom program written via the SDK that can be run on the attack drone. Approximate WiFi broadcast distance with a consumer cellphone receiver is approximately 0.5 miles.

#### Notes:
Unaffected by recent firmware update, and DJI is unlikely to require a cable to be plugged in in the future for the P3, so this process should work far into the future.

#### Limitations:

* A strong SSID password will take longer to crack, but can potentially be done using a cloud/server-side solution or with more advanced military hardware.

* Certain post-takeover options (Waypoint, POI, etc.) may be unavailable depending on the flight mode set by the controller.

#### Steps:

1. Scan for any Phantom SSID or MAC address

2. Connect to controller using default wireless key

    1. If connected, continue;

    2. If connection fails, brute-force wireless key

3. (Optional) Connect via FTP using default root password. It is extremely unlikely that this will fail as the default password cannot be changed easily (must be done through the filesystem).

    3. If connected, continue;

    4. If connection fails, send continuous deauth packets using AirCrack and skip step #4.

4. (Optional) Change default wireless password to prevent pilot reconnection - this is a preventative measure to ensure that we can connect before the pilot or his device attempts a reconnect. Can only been done if FTP connection succeeds.

    5. Change default wireless password by editing the filesystem.

    6. Trigger a reboot by writing to /proc/sysrq-trigger. This deauthenticates the pilot’s wireless device while applying our changes from the previous step. **This reboot can be done while in flight without causing the drone to crash, allowing us to execute a variety of code "on the fly".**

5. Connect our wireless device to the controller. Now that the pilot’s wireless device is disconnected from the network, we can connect using own wireless device and perform a desired action:

    7. Return to Home - The drone will be piloted back to the area in which it took off.  

        1. This will allow for physical  identification of the pilot’s location

        2. This will send the drone to a presumably safer area.

        3. Could be used in conjunction with the DCIM Malware program (pilot will have no idea).

    8. Change controller settings to make the drone unflyable, degrading (manual) flight mode

        4. Stick mode

        5. Gain & Expo Tuning

            1. Exponential Curve (EXP) tuning

            2. Sensitivity

    9. Change altitude settings

    10. Change core settings

    11. Advanced directives - available if pilot is flying in "F" mode (Advanced Programmatic mode)

        6. Launch Point of Interest (POI) feature, forcing a continuous circle of flight.

        7. Launch Follow Me feature, redirecting the drone to OUR wireless device.

            3. Long-term: We can develop our own app using the SDK that would run on the attack drone, causing the target drone to "follow" us wherever we go.

            4. Note: If the user is not in F (Advanced Programmatic) mode (toggled from the controller), these advanced features will not work as modes cannot be changed from within the app.

        8. Waypoint mode

    12. Pull flight logs (intel)

    13. Get model/serial number in the "Other" section (to track back to purchaser)

------

### "Intel" Program (subroutine)

#### Description:
Download identifying files from drone prior to drone destruction and store them on our device (Pi).

* Past wireless network activity

* All files from DCIM

* Other key directories in order of priority (var, etc, etc.)

* Grabs MAC address

* Grabs images/video from camera

------

### "Reward/Recovery" Program (subroutine)

#### Description:
Replace contents of DCIM with a "reward if found" identification image (with instructions for returning drone) prior to destruction in case the physical drone remains cannot be recovered by us. This allows for physical inspection of the drone to recover (fingerprints, serial number, etc.) if the payload has not detonated and if the drone.

## Planned Programs (to be coded)

### "Hail Mary" Program

#### Purpose:
Cause the drone to crash by destroying its filesystem.

#### Description:
As a last ditch effort, we will permanently brick all 3 filesystems (controller, drone, and camera). The pilot is now limited to manual (A) LOS flight.

------

### "DCIM Malware" Program

#### Description:
We place "image malware" on the drone. It can infect the pilot’s device if he either pulls images mid-flight or if the droneis returned to/retrieved by the pilot for one of a number of reasons:

* The pilot aborts the mission for an unknown reason.

* We’ve called Return to Home through one of our programs.

* The pilot notices our attempts to take control (unlikely) and calls the mission off using manual flight mode.

* The drone has crashed (by reason of pilot or us).

The pilot eventually retrieves contents from the DCIM, or transfers images to his wireless device mid-flight, and our image malware infects his machine and broadcasts data to lead to his location.

#### Possible Execution Methods:

* Masked file extension (cat.jpg.exe)

* EXIF/metadata exploits affecting specific programs (Windows Photo Viewer, etc.)

* base_64 encoded malware inside EXIF data, decoded by metadata method to infect websites where the image might be uploaded (see: https://blog.sucuri.net/2013/07/malware-hidden-inside-jpg-exif-headers.html)

------

### "Evil Twin" Program

#### Description:
Spoof the original controller’s MAC address, IP, SSID, encryption key, type and connection to take control of the drone using a new controller.

------

### "Line-of-Sight Disruption" Program

#### Purpose:
Degrade the "Line-of-sight" (LOS) Atti (manual) flight mode severely by making the drone invisible (at night) or making its visual position misleading (during the day). Assumes the attack will be carried out at least 100 yards.

#### Description:
Video transmission has already been disabled (either by us modifying the filesystem or by forcing a deauth continuously). The pilot must now resort to flying the drone manually via LOS. We will now make manual LOS flight impossible at night and nearly impossible during the day. We disable or modify LED behavior to degrade this line-of-sight manual flight mode:

* Nighttime flying: Disable LEDs entirely, rendering the aircraft invisible.

* Daytime flying: Increment or randomize LED position by one either clockwise or counterclockwise, in a random order, and/or make all LEDs a solid color, thus making craft yaw difficult to determine.

------

### Force RTH

#### Purpose:
Force return to home, returning the device to the pilot and away from his intended target.

#### Description:
Jam RF, forcing the default behavior of returning to home (unless this setting is changed in the app to "Hover"). The drone will return to home or hover after 3 seconds.

------

### "Find the Pilot" Program

#### Purpose:
Locate the pilot of a DJI Phantom drone so that SOF can apprehend him.

#### Description:
Using our drone’s GPS and a sweeping flight pattern, we can monitor the signal strength of the pilot’s wireless network (without even being connected to it), thus locating the pilot and broadcasting his coordinates to relevant parties for retrieval.

## Disclaimer
Do not use this software for illegal purposes. It was developed for and is being provided as part of a research project. Signal spoofing and/or jamming is illegal in most countries -- don't do illegal things.

## License (GNU GPL)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
