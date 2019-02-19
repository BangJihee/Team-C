'''
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


    def sensor_output():
        return sensor_output.copy()


    for i in range(4):
        gpio.pinMode(gpiopins[i], gpio.OUTPUT)
    #c1 temp
    gpio.digitalWrite(gpiopins[0], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[1], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[2], 0)
    sleep(0.5)
    gpio.digitalWrite(gpiopins[3], 0)
    sleep(0.5)

    v = raw * scale
    temp = (v - 500) / 10 - 6
    #Celsius to Fehrenheit formula
    temp= temp*1.8 + 32


    sleep(1)

    while True:
        for client_handler in server.active_client_handlers.copy():

            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"

            #time
            epoch_time = int(time())
            sensor_output['TIme'] = epoch_time

            #real-time temperature
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            v = raw * scale
            temp =  (v - 500) / 10 - 6
            # Celsius to Fehrenheit formula
            temp = temp * 1.8 + 32
            print(temp)


            #Sensor read the value
            logger.info("Reading sensor :{}".format(sensor_type[0],temp))
            sensor_output[sensor_type[0]]=temp

            #c2

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




            PM25 = uniform(120, 130)    # random PM25 value

            msg = ""

            if args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': temp,
                          'SN1': SN1,
                          'SN2': SN2,
                          'SN3': SN3,
                          'SN4': SN4,
                          'PM25': PM25}
                msg = json.dumps(output)
            elif args.output_format == "csv":
                msg = "realtime, {}, {}, {}, {}, {}, {}, {}".format(epoch_time, temp, SN1, SN2, SN3, SN4, PM25)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 2 seconds
        sleep(2)
'''
import logging
import sqlite3
from neo import Gpio
from threading import Thread
from threading import Lock
from time import sleep, time

logger = logging.getLogger(__name__)


class SensorServer(Thread):
    """Sensor server that keeps reading sensors and provide get_sensor_output() method for user"""

    def __init__(self, database_name="air_pollution_data.db"):
        # Parent class constructor
        Thread.__init__(self)

        # Assign GPIO pins that controls MUX, LSB to MSB
        self.gpio_pins = [24, 25, 26, 27]
        self.gpio = Gpio()
        # Set GPIO pins to output
        try:
            for pin in self.gpio_pins:
                self.gpio.pinMode(pin, self.gpio.OUTPUT)
        except Exception as e:
            logger.error("Error setting GPIO pin {}, reason {}".format(pin, e.message))

        # Use A0 port
        self.adc_raw = "/sys/bus/iio/devices/iio:device0/in_voltage0_raw"
        self.adc_scale = "/sys/bus/iio/devices/iio:device0/in_voltage_scale"

        self.sensor_names = ['temp', 'NO2', 'O3', 'CO', 'SO2', 'PM25']

        # Use a dict to store sensor output, the format is:
        # { "time": [time stamp],
        #   [sensor1 name]: [sensor1 output],
        #   ...
        #   [sensor6 name]: [sensor6 output]}
        self.sensor_output = {}

        # Create a lock to protect sensor output. That is, when updating the result, lock it on to prevent it from being
        # read at the same time; similarly, when reading the result, lock it on to prevent it from being updated.
        self.sensor_output_lock = Lock()

        # Here we have a decision to make. I decide to let sensor server write sensor outputs to the local database. Of
        # course we can do so in a different thread either in a synchronous way or in an asynchronous way. If we do it
        # with a synchronous approach, we need to use locks to keep synchronization; if we do it with an asynchronous
        # solution, then SQLite3 is already an asynchronous module and I don't see good reason of adding another layer
        # of complexity. Perhaps the most reasonable way would be specifying the database in the main thread and then
        # send it to the sensor server thread.
        self.database_name = database_name

        try:
            # Create the database file and get the connection object.
            self.db_conn = sqlite3.connect(self.database_name)
            # Get database cursor from the connection object.
            self.db_cur = self.db_conn.cursor()
        except Exception as e:
            logger.error("Error connecting the database {}, reason: {}".format(self.database_name, e.message))
            self.__del__()

        # Create a 'history' table for history data.
        #  TIME | Temp |  SN1 |  SN2 |  SN3 |  SN4 | PM25
        # -----------------------------------------------
        #   int | real | real | real | real | real | real
        self.db_cur.execute(("CREATE TABLE IF NOT EXISTS history (time int PRIMARY KEY NOT NULL,"
                             " {0} real, {1} real, {2} real, {3} real, {4} real, {5} real)")
                            .format(self.sensor_names[0],
                                    self.sensor_names[1],
                                    self.sensor_names[2],
                                    self.sensor_names[3],
                                    self.sensor_names[4],
                                    self.sensor_names[5]))

        # Commit the changes. When a database is accessed by multiple connections, and one of the processes modifies the
        # database, the SQLite database is locked until that transaction is committed. The timeout parameter specifies
        # how long the connection should wait for the lock to go away until raising an exception. The default for the
        # timeout parameter is 5.0 (five seconds).
        self.db_conn.commit()

    def __del__(self):
        # Gracefully close the database connection.
        self.db_conn.close()
        # Reset GPIOs.
        for i in xrange(0, 4):
            self.gpio.digitalWrite(24 + i, Gpio.LOW)

    def get_sensor_output(self):
        # Get the latest sensor output
        return self.sensor_output.copy()

    def set_mux_channel(self, m):
        # Set MUX channel
        # Convert n into a binary string
        bin_repr = "{0:04b}".format(m)
        # Assign value to pin
        for i in xrange(0, 4):
            self.gpio.digitalWrite(24 + i, bin_repr[i])

    def read_sensor(self, n):
        # Read raw data from sensor n, we allocate 2 channels for each sensor:
        # sensor 0: channel 0, 1
        # sensor 1: channel 2, 3
        # ...
        # sensor 7: channel 15, 16

        # Set MUX to read the first channel
        try:
            self.set_mux_channel(2 * n)
            # Wait for 50 ms
            sleep(0.05)
            v1 = int(open(self.adc_raw).read()) * float(open(self.adc_scale).read())

            # Set MUX to read the second channel
            self.set_mux_channel(2 * n + 1)
            sleep(0.05)
            v2 = int(open(self.adc_raw).read()) * float(open(self.adc_scale).read())

            return v1, v2
        except Exception as e:
            logger.error("Error reading sensor {}, reason: {}".format(n, e.message))
            return 0.0, 0.0

    def run(self):
        try:
            # Create the database file and get the connection object.
            self.db_conn = sqlite3.connect(self.database_name)
            # Get database cursor from the connection object.
            self.db_cur = self.db_conn.cursor()
        except Exception as e:
            logger.error("Error connecting the database {}, reason: {}".format(self.database_name, e.message))
            self.__del__()

        # Keep reading sensors.
        while True:
            # Acquire the lock
            self.sensor_output_lock.acquire()
            # Add time stamp
            epoch_time = int(time())
            self.sensor_output['time'] = epoch_time

            # Do sensor reading here
            #  1. set MUX to sensor 0, read sensor 0;
            #  2. set MUX to sensor 1, read sensor 1;
            #  ...
            #  n. set MUX to sensor n - 1, read sensor n - 1.
            logger.info("Reading {} sensor...".format(self.sensor_names[0]))
            # Temperature constant
            t0 = 500
            c0, c1 = self.read_sensor(0)
            # Channel 1 is not connected so we don't care about its output
            temp = c0 - t0
            temp = temp if (temp >= 0) else -temp
            logger.info("{} sensor outputs {} degree".format(self.sensor_names[0], temp))
            # Save output to the dict
            self.sensor_output[self.sensor_names[0]] = temp

            logger.info("Reading {} sensor...".format(self.sensor_names[1]))
            c2, c3 = self.read_sensor(1)
            sn1 = ((c2 - 295) - ((0.75) * (c3 - 282))) * 4.386
            sn1 = sn1 if (sn1 >= 0) else -sn1
            logger.info("{} sensor outputs {} ppb".format(self.sensor_names[1], sn1))
            # Save output to the dict
            self.sensor_output[self.sensor_names[1]] = sn1



            logger.info("Reading {} sensor...".format(self.sensor_names[2]))
            c4, c5 = self.read_sensor(2)
            sn2 = ((c4 - 391) - ((0.5) * (c5 - 390))) * 2.506
            sn2 = sn2 if (sn2 >= 0) else -sn2
            logger.info("{} sensor outputs {} ppb".format(self.sensor_names[2], sn2))
            # Save output to the dict

            self.sensor_output[self.sensor_names[2]] = sn2

            logger.info("Reading {} sensor...".format(self.sensor_names[3]))
            c6, c7 = self.read_sensor(3)
            sn3 = ((c6 - 347) - (0.44 * (c7 - 296))) * 0.0375
            sn3 = sn3 if (sn3 >= 0) else -sn3
            logger.info("{} sensor outputs {} ppb".format(self.sensor_names[3], sn3))
            # Save output to the dict
            self.sensor_output[self.sensor_names[3]] = sn3

            logger.info("Reading {} sensor...".format(self.sensor_names[4]))
            c8, c9 = self.read_sensor(4)
            sn4 = ((c8 - 345) - ((0.6) * (c9 - 255))) * 3.145
            sn4 = sn4 if (sn4 >= 0) else -sn4
            logger.info("{} sensor outputs {} ppb".format(self.sensor_names[4], sn4))
            # Save output to the dict
            self.sensor_output[self.sensor_names[4]] = sn4

            logger.info("Reading {} sensor...".format(self.sensor_names[5]))
            c10, c11 = self.read_sensor(5)

            pm25 = 0.518 + 0.00274*(240.0*(c10)**6 - 2491.3*(c10)**5 + 9448.7*(c10)**4 - 14840.0*(c10)**3 + 10684.0*(c10)**2 + 2211.8*(c10) + 7.9623)*1.5*10**(-16)
            logger.info("{} sensor outputs {} ppb".format(self.sensor_names[5], pm25))
            # Save output to the dict
            self.sensor_output[self.sensor_names[5]] = pm25

            self.db_cur.execute("INSERT INTO history VALUES ({},{}, {}, {}, {}, {}, {})"
                                .format(epoch_time, temp, sn1, sn2, sn3, sn4, pm25))

            self.db_conn.commit()
            self.sensor_output_lock.release()

            # Idle for 3 seconds
            sleep(1.8)
