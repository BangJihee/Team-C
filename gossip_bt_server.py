'''from btserver import BTServer
from bterror import BTError
from Sensor import SensorServer

import argparse
import asyncore
import json
import logging
import sqlite3

from random import uniform
from threading import Thread
from time import sleep, time,gmtime,strftime

logger=logging.getLogger(__name__)

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    parser.add_argument("--database", dest="database_name",default="air_pollution_data.db", help="specify data file")
    parser.add_argument("--baud_rate", default="115200", help="specify bluetooth baud rate in bps")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    bt_service_name = "Air Pollution Sensor"
    bt_server = BTServer(uuid, bt_service_name)

    # Create the server thread and run it
    bt_server_thread = Thread(target=asyncore.loop, name="Blutooth Server Thread")
    bt_server_thread.daemon = True
    bt_server_thread.start()

    #Create sensor server thread and run it
    sensor_server=SensorServer(database_name=args.database_name)
    sensor_server.daemon=True
    sensor_server.start()

    #Create database connenction and retrieve its cursor
    try:
        db_conn=sqlite3.connect(args.database_name)
        db_cur = db_conn.cursor()
    except Exception as e:
        logger.error("Error : Connecting the database{},reason : {}".format(args.database_name.e.message))

    #data loop

    while True:
        msg=" "
        sensor_output=sensor_server.get_sensor_output()
        epoch_time=int(time())
        temp = sensor_output.get('Temp', -1)  #  temperature
        NO2 =sensor_output.get('NO2', -1)  #  SN1 NO2 value
        O3 = sensor_output.get('O3', -1)  # SN2 O3 value
        CO = sensor_output.get('CO', -1)  #  SN3 Co value
        SO2 = sensor_output.get('SO2', -1)  #  SN4 SO2 value
        PM25 = sensor_output.get('PM25', -1)  #  PM25 value

        r_msg=" "
        if args.output_format=="cvs":
            r_msg=" {} ,{} , {} , {} , {} , {} , {} ".format(epoch_time.teemp,NO2,O3,CO,SO2,PM25)
        elif args.output_format=="json":
            output={'time' : epoch_time,
                    'NO2' : NO2,
                    'O3' : O3,
                    'CO' : CO,
                    'SO2' : SO2,
                    'PM25' : PM25
            }
            r_msg=json.dumps(output)

        for client_handler in bt_server.active_client_handlers():
            if client_handler.sending_status.get('History')[0]:
                start_time=client_handler.sending_status.get('History')[1]
                end_time=client_handler.sending_status.get('History')[2]
                fmt_start_time=strftime("%Y-%M-%D %H:%M:%S",gmtime(start_time))
                fmt_end_time=strftime("%Y-%M-%D %H:%M:%S",gmtime(end_time))

                logger.info("Client request history between {} and {}".format(fmt_start_time,fmt_end_time))
                print("INFO:Client request history between {} and {}".format(fmt_start_time,fmt_end_time))

                if start_time > end_time:
                    logger.warn("Start time {} is better than end time{}, skipping...".format(fmt_start_time,fmt_end_time))
                    print("WARN :Start time {} is better than end time{}, skipping...".format(fmt_start_time,fmt_end_time))

                elif db_cur is None:
                    logger.error("SQL database {} is not availble".format(args.database_name))
                    print("ERROR: SQL database {} is not availble".format(args.database_name))

                else:
                    db_cur.execute("SELECT *FROM history WHERE TIme>={} AND Time<={}".format(start_time,end_time))

                    results=db_cur.fetchall()
                    n=len(results)

                    logger.info("Number of data points in the result is {} ,sending them at {}bps".format(n,args.baud_rate))
                    print("INFO :Number of data points in the result is {} ,sending them at {}bps".format(n,args.baud_rate))

                    i=0
                    print ("INFO : SENDING  result(0/0)...\r")
                    for row in results:
                        i +=1
                        h_msg="{},{},{},{},{},{},{}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                        client_handler.send('h'+ h_msg +'\n')

                        print("INFO : sending results ({}/{}) ...\r".format(i,n))
                        sleep(((len(h_msg)+2)*8*1.1/int(args.baud_rate)))


                        print("\nINFO : Done")
                        client_handler.send("h\n")
                    client_handler.sending_status['History']=[False,-1,-1]
            elif client_handler.sending_status.get('realtime'):
                try:
                    client_handler.send(('r'+r_msg+'\n'))
                except Exception as e:
                    BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                    client_handler.handle_close()

            # Sleep for 3 seconds
            sleep(1)
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
    neo.digitalWrite(pinNum[2], 1)
    sleep(0.5)
    neo.digitalWrite(pinNum[3], 1)
    sleep(0.5)

    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
    v = raw * scale
    t = (v - 500) / 10 - 6

    t= t*1.8 + 32

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
