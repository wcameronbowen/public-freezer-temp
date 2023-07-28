# public-freezer-temp

## Use Case
Monitor temperature and power in freezer (or other appliance) and send text/email alerts when it falls out of range

## Hardware
1. raspberry pi pico w
1. [pimoroni lipo shim](https://shop.pimoroni.com/products/pico-lipo-shim)
1. battery for shim
1. ds1820 temp sensor

### Instruction
1. Copy `secrets.py.example` to `secrets.py` and fill out with appropriate credentials/config
1. Copy `secrets.py`, `main.py`, and `umail.py` to pico root directory
1. Connect lipo shim per instructions to pico
1. Connect ds1820 temp sensor to pin 28 for sending data
1. Boot it up!
