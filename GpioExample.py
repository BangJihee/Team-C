from neo import Gpio  # import Gpio library
from time import sleep  # import sleep to wait for blinks


neo =Gpio()

S0 = 24 # pin to use
S1 = 25
S2 = 26
S3 = 27

pinNum = [S0, S1, S2, S3]

num = [0,0,0,0]

# Blink example
for i in range(4):
    neo.pinMode(pinNum[i], neo.OUTPUT)

neo.digitalWrite(pinNum[0], 0)
sleep(0.5)
neo.digitalWrite(pinNum[1], 0)
sleep(0.5)
neo.digitalWrite(pinNum[2], 1)
sleep(0.5)
neo.digitalWrite(pinNum[3], 1)
sleep(0.5)

raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
v = raw * scale
t = (v - 500) / 10 - 6
sleep(1)
print(t)

'''
raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
print (raw * scale)
'''


