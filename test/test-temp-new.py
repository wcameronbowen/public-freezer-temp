from machine import Pin
import time, ds18x20
import onewire

ow = onewire.OneWire(Pin(2)) # create a OneWire bus on GPIO12
#ow_selected = ow.scan()               # return a list of devices on the bus
# ow.reset()              # reset the bus
# ow.readbyte()           # read a byte
# ow.writebyte(0x12)      # write a byte on the bus
# ow.write('123')         # write bytes on the bus
# ow.select_rom(b'(\xff\xdcK\xb2\x17\x01l') # select a specific device by its ROM code

ds = ds18x20.DS18X20(ow)
roms = ds.scan()
ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(ds.read_temp(rom))