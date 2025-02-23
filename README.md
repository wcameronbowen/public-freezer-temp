# public-freezer-temp

## Use Case
Monitor temperature and power in freezer (or other appliance) and send text/email alerts when it falls out of range

## Hardware
1. raspberry pi pico w
1. [pimoroni lipo shim](https://shop.pimoroni.com/products/pico-lipo-shim)
1. battery for shim
1. ds1820 temp sensor

## Initialize Pico (Mac)
> [!WARN] 
> if your code is named `main.py` on the pico it will run indefinitely. To exit while connected, use CTRL + C to enter the python REPL. If that does not work, you may have added a catch for `KeyboardInterrupt`, see [this forum](https://forums.raspberrypi.com/viewtopic.php?t=305432#p1827786). You'll probably have to [nuke your pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory). The rescue firmware [here](https://forums.raspberrypi.com/viewtopic.php?t=305432) does not work on a pico w.

1. make sure you install drivers for FTDI chips on a new system
```
brew install ftdi-vcp-driver
```
1. plug in the pico using the microUSB port
1. check your devices for a usb device
```
$ ls /dev | grep usb
cu.usbmodem101
tty.usbmodem101
```
pip3 install rshell
```
1. Copy `secrets.py.example` to `secrets.py` and fill out with appropriate credentials/config
```
cp secrets.py.example secrets.py
```
1. Copy `secrets.py`, `main.py`, and `umail.py` to pico root directory
```
rshell --quiet --port /dev/tty.usbmodemxxx cp ./*.py /pyboard/
```
1. Connect lipo shim per instructions to pico
1. Connect ds1820 temp sensor to pin 28 for sending data
1. Boot it up!
