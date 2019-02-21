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
from json import dumps
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

    pinnum = [0, 0, 0, 0]
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
            sleep(0.05)

            # real-time temperature
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())


            c0 = raw * scale
            t = (c0 - 500) / 10 - 6
            # Celsius to Fehrenheit formula
            t = t * 1.8 + 32

            print("Temp: {} F".format(t))

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
            sleep(0.05)

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

            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c3 = raw * scale


            SN1 = ((c2 - 220) - ((1.18) * (c3 - 260))) / 0.207
            SN1 = SN1 if (SN1 >= 0) else -SN1
            print("NO2 _SN1 : {}".format(SN1))

            #c4
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.05)

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
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c5 = raw * scale


            SN2 = ((c4 -414 ) - ((0.18) * (c5 - 400))) / 0.256
            SN2 = SN2 if (SN2 >= 0) else -SN2
            print("O3 _SN2 : {}".format(SN2))


            #c6
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 1)
            gpio.digitalWrite(gpiopins[2], 1)
            gpio.digitalWrite(gpiopins[3], 0)
            sleep(0.05)

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
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c7 = raw * scale


            SN3 =(((c6 - 346) - ((0.03) * (c7 - 274))) / 0.276)/1000
            SN3 = SN3 if (SN3 >= 0) else -SN3
            print("CO_SN3 : {}".format(SN3))

            #c8
            for i in range(4):
                gpio.pinMode(gpiopins[i], gpio.OUTPUT)
            gpio.digitalWrite(gpiopins[0], 0)
            gpio.digitalWrite(gpiopins[1], 0)
            gpio.digitalWrite(gpiopins[2], 0)
            gpio.digitalWrite(gpiopins[3], 1)
            sleep(0.05)

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
            sleep(0.05)

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
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c11 = (raw * scale)/1000

            PM25 = float((240.0*pow(c11,6) - 2491.3*pow(c11,5) + 9448.7*pow(c11,4) - 14840.0*pow(c11,3) + 10684.0*pow(c11,2) + 2211.8*c11 + 7.9623))
            PM25 = 0.518 + .00274 * PM25
            PM25 = PM25 if (PM25 >= 0) else -PM25
            print("PM25 : {}".format(PM25))

            msg = ""
            #AQI Conversion

            def AQI_CALCULATION(Imin, Imax, Cmin, Cmax, Input):
                Result = ((float(Imax) - float(Imin)) / (float(Cmax) - float(Cmin))) * (float(Input) - float(Cmin)) + float(Imin)
                return float(Result)


            def O3(num):
                if 0 <= num and num >= 54:
                    return AQI_CALCULATION(0, 50, 0, 54, num)
                elif 55 <= num and num >= 70:
                    return AQI_CALCULATION(51, 100, 55, 70, num)
                elif 71 <= num and num >= 85:
                    return AQI_CALCULATION(101, 150, 71, 85, num)
                elif 86 <= num and num >= 105:
                    return AQI_CALCULATION(151, 200, 86 ,105, num)
                elif 106 <= num and num >= 200:
                    return AQI_CALCULATION(201, 300, 106, 200, num)

            def A_PM25(num):
                if 0.0 <= num and num >= 12.0:
                    return AQI_CALCULATION(0, 50, 0.0, 12.0, num)
                elif 12.1<=num and num>=35.4:
                    return AQI_CALCULATION(51, 100, 12.1, 35.4, num)
                elif 35.5<=num and num >=55.4:
                    return AQI_CALCULATION(101, 150, 35.5, 55.4, num)
                elif 55.5<=num and num >=150.4:
                    return AQI_CALCULATION(151, 200, 55.5, 150.4, num)
                elif 150.5<=num and num >=250.4:
                    return AQI_CALCULATION(201, 300 ,150.5, 250.4, num)
                elif 250.5<=num and num >=350.4:
                    return AQI_CALCULATION(301, 400, 250.5, 350.4, num)
                elif 350.5<=num and num >=500.4:
                    return AQI_CALCULATION(401, 500, 350.5, 500.4, num)


            def CO(num):
                if 0<=num and num>=4.4:
                    return AQI_CALCULATION(0, 50, 0, 4.4, num)
                elif 4.5<=num and num>=9.4:
                    return AQI_CALCULATION(51, 100, 4.5, 9.4, num)
                elif 9.5<=num and num >=12.4:
                    return AQI_CALCULATION(101, 150, 9.5, 12.4, num)
                elif 12.5<=num and num >=15.4:
                    return AQI_CALCULATION(151, 200, 12.5, 15.4, num)
                elif 15.5<=num and num >=30.4:
                    return AQI_CALCULATION(201, 300, 15.5, 30.4, num)
                elif 30.5<=num and num >=40.4:
                    return AQI_CALCULATION(301, 400, 30.5, 40.4, num)
                elif 40.5<=num and num >=50.4:
                    return AQI_CALCULATION(401, 500, 40.5, 50.4, num)


            def SO2(num):
                if 0 <= num and num >= 35:
                    return AQI_CALCULATION(0, 50, 0, 35, num)
                elif 36 <= num and num >= 75:
                    return AQI_CALCULATION(51, 100, 36, 75, num)
                elif 76 <= num and num >= 185:
                    return AQI_CALCULATION(101, 150, 76, 185, num)
                elif 186 <= num and num >= 304:
                    return AQI_CALCULATION(151, 200, 186, 304, num)
                elif 305 <= num and num >= 604:
                    return AQI_CALCULATION(201, 300, 305, 604, num)
                elif 605 <= num and num >= 804:
                    return AQI_CALCULATION(301, 400, 605, 804, num)
                elif 805 <= num and num >= 1004:
                    return AQI_CALCULATION(401, 500, 805, 1004, num)


            def NO2(num):
                if 0 <= num and num >= 53:
                    return AQI_CALCULATION(0, 50, 0, 53, num)
                elif 54 <= num and num >= 100:
                    return AQI_CALCULATION(51, 100, 54, 100, num)
                elif 101 <= num and num >= 360:
                    return AQI_CALCULATION(101, 150, 101, 300, num)
                elif 361 <= num and num >= 649:
                    return AQI_CALCULATION(151, 200, 301, 649, num)
                elif 650 <= num and num >= 1249:
                    return AQI_CALCULATION(201, 300, 650, 1249, num)
                elif 1250 <= num and num >= 1649:
                    return AQI_CALCULATION(301, 400, 1250, 1649, num)
                elif 1650 <= num and num >= 2049:
                    return AQI_CALCULATION(401, 500, 1650, 2049, num)

            AQI_NO2 = NO2(SN1)
            print("AQI_NO2:{} ".format(int(AQI_NO2)))

            AQI_O3 = O3(SN2)
            print("AQI_O3:{}".format(int(AQI_O3)))

            AQI_CO = CO(SN3)
            print("AQI_CO:{}".format(int(AQI_CO)))

            AQI_SO2 = SO2(SN4)
            print("AQI_SO2 : {}".format(int(AQI_SO2)))

            AQI_PM25 = A_PM25(PM25)
            print("AQI_PM25: {.2f}".format(AQI_PM25))


            #now = datetime.now()
            #now = dumps(datetime.now(), default=json_serial)

            if args.output_format == "json":
                output = {
                          'time': epoch_time,
                          'temp': round(t), #real temperature
                          'SN1': SN1, #NO2
                          'SN2': SN2, #O3
                          'SN3': SN3, #CO
                          'SN4': SN4, #SO2
                          'PM25': PM25,
                          'A_SN1': round(AQI_NO2),
                          'A_SN2': round(AQI_O3),
                          'A_SN3': round(AQI_CO),
                          'A_SN4': round(AQI_SO2),
                          'A_PM25': round(AQI_PM25)

                }
                msg = json.dumps(output)
            elif args.output_format == "csv":
                msg = "Time:{}, {}, {}, {}, {}, {}, {}, {} ,{}, {}, {} , {} ".format(epoch_time, t, SN1, SN2, SN3, SN4 ,AQI_NO2,AQI_O3,AQI_O3,AQI_CO,AQI_SO2, AQI_PM25)
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
        sleep(2.5)
