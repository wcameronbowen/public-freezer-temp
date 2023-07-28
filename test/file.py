from machine import ADC
from machine import Pin
import random
import utime

tempsensor = ADC(machine.ADC.CORE_TEMP)
#pin = Pin(25, Pin.OUT)convert = 3.3 / (65535)rndfilenm = random.randrange(10000)file = open(str(rndfilenm) + “-tempdata.txt”, “w”)
pin = Pin('WL_GPIO0', Pin.OUT)

convert = 3.3 / (65535)

rndfilenm = random.randrange(10000)
print(rndfilenm)
file = open(str(rndfilenm) + '-tempdata.txt', 'w')

while True:
    pin.value(1)
    tempvalue = tempsensor.read_u16() * convert
    print(tempvalue)
    celsius = 27 - (tempvalue - 0.706) / 0.001721
    fahrenheit = round((celsius * 1.8) + 32, 2)
    print(fahrenheit)
    file.write(str(fahrenheit) + ',')
    file.flush()
    pin.value(0)
    utime.sleep(5)