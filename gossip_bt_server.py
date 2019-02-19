from btserver import BTServer
from bterror import BTError
from neo import Gpio
import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time
import logging
import sqlite3


logger= logging.getLogger(__name__)
#Allows the application log to integrate its own messages with messages from third module
if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="json", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "BTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    #Assign GPIO pin to use & controls Mux board
    #S0 = 24  # pin to use
    #S1 = 25
    #S2 = 26
    #S3 = 27
    #pinNum = [S0, S1, S2, S3]
    gpiopins=[24,25,26,27]
    gpio = Gpio()

    num = [0, 0, 0, 0]
    sensor_type=['Temp','NO2','O3','CO','SO2','PM25']

    # Using A0 pin
    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

    #Set GPIO pins to output
    try:
        for pin in gpiopins:
            gpio.pinMode(pin,gpio.OUTPUT)
    except Exception as e:
        logger.error("Error : GPIO pin {} .reason {}".format(pin,e.message))


    #def sensor_output():
    #    return sensor_output.copy()

    #sqlite Database
    conn=sqlite3.connect('air_quality_data.db')
    c=conn.cursor()

    #Create table
    #c.execute("CREATE TABLE IF NOT EXISTS HISTORY Data")

    for i in range(4):
        gpio.pinMode(gpiopins[i], gpio.OUTPUT)
    #c0 temp
    gpio.digitalWrite(gpiopins[0], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[1], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[2], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[3], 0)
    sleep(0.5)

    v = raw * scale
    t = (v - 500) / 10 - 6
    #Celsius to Fehrenheit formula
    t= t*1.8 + 32

    sleep(1)

    while True:
        for client_handler in server.active_client_handlers.copy():

            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"

            #time
            epoch_time = int(time())
            #sensor_output['TIme'] = epoch_time

            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            # c0 temp
            gpio.digitalWrite(gpiopins[0], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            # real-time temperature
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

            v = raw * scale
            t = (v - 500) / 10 - 6
            # Celsius to Fehrenheit formula
            t = t * 1.8 + 32

            print(t)

            #Sensor read the value
            logger.info("Reading sensor :{}".format(sensor_type[0],t))
            #sensor_output[sensor_type[0]]=t

            #c2
            #SN1=((c2 - Vwe)-((n)*(c3-Vae)))*a
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)


            #raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            #scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            #v = raw * scale


            #c3
            gpio.digitalWrite(gpiopins[0], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)
            SN1 = uniform(40, 50)       # random SN1 value


            #c4
            gpio.digitalWrite(gpiopins[0], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            #c5
            gpio.digitalWrite(gpiopins[0], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)


            SN2 = uniform(60, 70)       # random SN2 value

            #c6
            gpio.digitalWrite(gpiopins[0], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            #c7
            gpio.digitalWrite(gpiopins[0], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            SN3 = uniform(80, 90)       # random SN3 value

            #c8
            gpio.digitalWrite(gpiopins[0], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.5)

            #c9
            gpio.digitalWrite(gpiopins[0], 1)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[1], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[2], 0)
            sleep(0.5)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.5)


            SN4 = uniform(100, 110)     # random SN4 value



            #PM sensor
            PM25 = uniform(120, 130)    # random PM25 value

            msg = ""

            if args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': t,
                          'SN1': SN1,
                          'SN2': SN2,
                          'SN3': SN3,
                          'SN4': SN4,
                          'PM25': PM25}
                msg = json.dumps(output)
            elif args.output_format == "csv":
                msg = "realtime, {}, {}, {}, {}, {}, {}, {}".format(epoch_time, t, SN1, SN2, SN3, SN4, PM25)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, oerrr=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()


            # Insert a row of data
            c.execute("INSERT INTO history data {},{},{},{},{},{},{}".format(epoch_time, t, SN1, SN2, SN3, SN4, PM25))

            # Save (commit) the changes
            conn.commit()

            # User can close the connection if user are done with it
            conn.close()

            # Sleep for 2 seconds
        sleep(2)
