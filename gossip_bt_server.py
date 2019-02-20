from btserver import BTServer
from bterror import BTError
from neo import Gpio
import argparse
import asyncore
import json
from threading import Thread
from time import sleep, time
import logging
import sqlite3

from datetime import datetime
from json import dumps

logger= logging.getLogger(__name__)
#Allows the application log to integrate its own messages with messages from third module
if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="json", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a Air pollution sensor server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "Air pollution sensor"
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
    #sensor_type=['Temp','NO2','O3','CO','SO2','PM25']

    # Using A0 pin
    #raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    #scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

    #Set GPIO pins to output
    try:
        for pin in gpiopins:
            gpio.pinMode(pin,gpio.OUTPUT)
    except Exception as e:
        logger.error("Error : GPIO pin {} .reason {}".format(pin,e.message))

    # Create database connection using cursor-sqlite Database
    try:
        db_conn = sqlite3.connect('air_quality_data.db')
        db_c = db_conn.cursor()
    except Exception as e:
        logger.error("Connecting error with the database {} ,reason {} ".format(args.database_name, e.message))

        # Create table
        # Time | Temp   | SN1    | SN2   | SN3    | SN4    | PM25
        # in  | r_data | r_data | r_data| r_data | r_data | r_data
     #db_c.execute(
     #   "CREATE TABLE IF NOT EXISTS HISTORY Data { } r_data,{ } r_data,{ } r_data,{ } r_data,{ } r_data,{ } r_data,{ } r_data,").format(sensor_type[0], sensor_type[1], sensor_type[2], sensor_type[3], sensor_type[4], sensor_type[5],
     #   sensor_type[6])


    #def sensor_output():
    #return sensor_output.copy()

    #Create table
    #c.execute("CREATE TABLE IF NOT EXISTS HISTORY Data")


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
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            # real-time temperature
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())


            c0 = raw * scale
            t = (c0 - 500) / 10 - 6
            # Celsius to Fehrenheit formula
            t = t * 1.8 + 32

            print("Temp: {}F".format(t))

            #Sensor read the value
            #logger.info("Reading sensor :{}".format(sensor_type[0],t))
            #sensor_output[sensor_type[0]]=t

            #c2
            #SN1=((c2 - Vwe)-((n)*(c3-Vae)))*a
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c2 = raw * scale

            #c3
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 1)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 0)

            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c3 = raw * scale


            SN1 = ((c2 - 290) - ((1.18) * (c3 - 284))) / 0.207
            SN1 = SN1 if (SN1 >= 0) else -SN1
            print("NO2 _SN1 : {}".format(SN1))

            #c4
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c4 = raw * scale


            #c5
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 1)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c5 = raw * scale


            SN2 = ((c4 -408 ) - ((0.18) * (c5 - 403))) / 0.256
            SN2 = SN2 if (SN2 >= 0) else -SN2
            print("O3 _SN2 : {}".format(SN2))


            #c6
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c6 = raw * scale



            #c7
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 1)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c7 = raw * scale


            SN3 =((c6 - 298) - ((0.03) * (c7 - 279))) / 0.276
            SN3 = SN3 if (SN3 >= 0) else -SN3
            print("CO_SN3 : {}".format(SN3))

            #c8
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c8 = raw * scale

            #c9
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 1)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c9 = raw * scale


            SN4 =((c8 - 300) - ((1.15) * (c9 - 292))) / 0.300
            SN4 = SN4 if (SN4 >= 0) else -SN4
            print("SO2_SN4 : {}".format(SN4))


            #PM sensor

            # c11
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 1)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.5)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c11 = (raw * scale)/1000


            PM25 = (240.0*pow(c11,6) - 2491.3*pow(c11,5) + 9448.7*pow(c11,4) - 14840.0*pow(c11,3) + 10684.0*pow(c11,2) + 2211.8*c11 + 7.9623)
            PM25 = PM25 if (SN4 >= 0) else -PM25
            print("PM25 : {}".format(PM25))

            msg = ""


            #AQI Conversion

            now = datetime.now();

            if args.output_format == "json":
                output = {
                          'time': now,
                          'temp': t, #real temperature
                          'SN1': SN1, #NO2
                          'SN2': SN2, #O3
                          'SN3': SN3, #CO
                          'SN4': SN4, #SO2
                          'PM25': PM25}
                msg = json.dumps(output)
            elif args.output_format == "csv":
                msg = "Time:{}, {}, {}, {}, {}, {}, {}, {}".format(now, t, SN1, SN2, SN3, SN4, PM25)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, oerrr=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()


            # Insert a row of data
            #db_c.execute("INSERT INTO history data {},{},{},{},{},{},{}".format(epoch_time, t, SN1, SN2, SN3, SN4, PM25))

            # Save (commit) the changes
            #db_conn.commit()

            # User can close the connection if user are done with it
            #db_conn.close()

            # Sleep for 1 seconds
            print("")
            print("")
        sleep(4.5)
