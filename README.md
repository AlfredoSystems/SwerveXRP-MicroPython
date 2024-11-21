# SwerveXRP-MicroPython
*v1.0.0*

This is code for my [XRP Differential Swerve Drive Robot](https://www.printables.com/model/950641-xrp-differential-swerve-drive-robot).

IMPORTANT: This code is a WIP. use at your own peril!

Right now each module can rotate and translate very well (what I consider the hard part) but all the modules rotate and translate the same, so the robot itself still can't rotate! I will find a few hours sometime eventually to figure out the final bit of fun vector math.

## Notes ##

- Both XRPs run the same code, except I give them both a different Bluetooth name. You can connect to either of them to drive the robot.
- The XRPs need a wired serial connection to communicate with each other. I used 3 Dupont female-female wires to connect D16->D17, D17->D16, and GND->GND
- The zero angle for each module is determined when the robot is turned on, all modules must be manually aligned at that time.
	- even if all the wheels are pointed the same way, some of them might be 180 degrees out of alignment. look for the small bevel gears for alignment.
- Huge props to FTC team 9048, this repo is not much more than a python version of their [java differential swerve drive code](https://github.com/ameliorater/ftc-diff-swerve?tab=readme-ov-file)

## SwerveXRP Setup Guide ##
1) Your robot needs [Pestolink-MicroPython](https://github.com/AlfredoSystems/PestoLink-MicroPython). Follow the first two steps in that repo. (doesn't hurt to go through all the steps just to get familiar with Pestolink).

1) Upload `Vector2D.py` to your XRP robot
	- [Click here](https://github.com/AlfredoSystems/SwerveXRP-MircoPython/archive/refs/heads/main.zip) to download this repository. After that, unzip it
	- In the XRP Code editor, go to `file > Upload to XRP` and select `Vector2D.py` from the repo you just downloaded
	- Save the file at the top level, so that `FINAL PATH: /Vector2D.py`

1) Upload `swervemodule.py` to your XRP robot
	- In the XRP Code editor, go to `file > Upload to XRP` and select `swervemodule.py` from the repo you just downloaded
	- Save the file at the top level, so that `FINAL PATH: /swervemodule.py`
	
1) Upload `swervemain.py` to your XRP robot
	- In the XRP Code editor, go to `file > Upload to XRP` and select `swervemain.py` from the repo you just downloaded
	- Save the file at the top level, so that `FINAL PATH: /swervemain.py`
	- change the `robot_name` string to what you want the robot to be named for Bluetooth pairing
	- Save the file again

1) Repeat the previous steps for the second XRP

1) Pairing and connecting
	- Go to [PestoLink-Online](https://pestol.ink).
	- Press/click `Connect BLE`. A pairing menu will appear, find and select the robot name you chose. After the connection opens, you can now drive your robot!
