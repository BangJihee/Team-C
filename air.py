from btserver import BTServer
from bterror import BTError
from neo import Gpio
import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    neo = Gpio()

    S0 = 24  # pin to use
    S1 = 25
    S2 = 26
    S3 = 27

    pinNum = [S0, S1, S2, S3]

    num = [0, 0, 0, 0]

    # Blink example
    for i in range(4):
        neo.pinMode(pinNum[i], neo.OUTPUT)


    neo.digitalWrite(pinNum[0], 0)
    sleep(0.5)
    neo.digitalWrite(pinNum[1], 0)
    sleep(0.5)
    neo.digitalWrite(pinNum[2], 0)
    sleep(0.5)
    neo.digitalWrite(pinNum[3], 0)
    sleep(0.5)

    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
    v = raw * scale
    t = (v - 500) / 10 - 6

    t= t*1.8 + 32

    print(t)

    sleep(1)


    while True:
        for client_handler in server.active_client_handlers.copy():

            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"


            #real-time temperature

            epoch_time = int(time())   # epoch time
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            v = raw * scale
            t = (v - 500) / 10 - 6

            t = t * 1.8 + 32

            print(t)

            SN1 = uniform(40, 50)       # random SN1 value
            SN2 = uniform(60, 70)       # random SN2 value
            SN3 = uniform(80, 90)       # random SN3 value
            SN4 = uniform(100, 110)     # random SN4 value
            PM25 = uniform(120, 130)    # random PM25 value

            msg = ""
            if args.output_format == "csv":
                msg = "realtime, {}, {}, {}, {}, {}, {}, {}".format(epoch_time, t, SN1, SN2, SN3, SN4, PM25)
            elif args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': t,
                          'SN1': SN1,
                          'SN2': SN2,
                          'SN3': SN3,
                          'SN4': SN4,
                          'PM25': PM25}
                msg = json.dumps(output)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 2 seconds
        sleep(2)
