'''from btserver import BTServer
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

        ############################ N table ####################################
        # array for calculate alph                                              ##
        # temp              -30,  -20   -10     0    10     20   30    40    50 ##
        # index               0,    1,    2,    3,    4,    5,    6,    7 ,   8 ##
        O3_tempArray = [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 2.87]  ##
        SO2_tempArray = [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 1.95]  ##
        NO2_tempArray = [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00, 2.70]  ##
        CO_tempArray = [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48, -0.80]  ##
        #########################################################################

        def get_alpha(temper, air):  # air = (NO2,O3, CO, SO2)
            temper
            i = 0  # index
            mulx = 0  # multiple #times
            if (-30 <= temper < -20):
                i = 0;
                mulx = temper + 30  # ex -28'C + 30 = 2 >> 2
            elif (-20 <= temper < -10):
                i = 1;
                mulx = temper + 20
            elif (-10 <= temper < 0):
                i = 2;
                mulx = temper + 10
            elif (0 <= temper < 10):
                i = 3;
                mulx = temper
            elif (10 <= temper < 20):
                i = 4;
                mulx = temper - 10
            elif (20 <= temper < 30):
                i = 5;
                mulx = temper - 20
            elif (30 <= temper < 40):
                i = 6;
                mulx = temper - 30
            elif (40 <= temper < 50):
                i = 7;
                mulx = temper - 40
            elif (50 <= temper):
                i = 8;  # if temperature exceed 50 just give 50'C data

            N = 0.0
            if (air == 'O3'):
                if (i == 8):
                    N = O3_tempArray[i]
                else:
                    tmp = (O3_tempArray[i + 1] - O3_tempArray[i]) / 10.0
                    N = O3_tempArray[i] + (tmp * mulx)

            elif (air == 'CO'):
                if (i == 8):
                    N = CO_tempArray[i]
                else:
                    tmp = (CO_tempArray[i + 1] - CO_tempArray[i]) / 10.0
                    N = CO_tempArray[i] + (tmp * mulx)

            elif (air == 'NO2'):
                if (i == 8):
                    N = NO2_tempArray[i]
                else:
                    tmp = (NO2_tempArray[i + 1] - NO2_tempArray[i]) / 10.0
                    N = NO2_tempArray[i] + (tmp * mulx)

            elif (air == 'SO2'):
                if (i == 8):
                    N = SO2_tempArray[i]
                else:
                    tmp = (SO2_tempArray[i + 1] - SO2_tempArray[i]) / 10.0
                    N = SO2_tempArray[i] + (tmp * mulx)

            return N

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

            print(c8)
            print(c9)


            #SN4 =((c8 - 300) - (get_n(t,'SO2')) * (c9 - 292)) / 0.300
            SN4 = ((c8 - 300) - (get_alpha(t, 'SO2')) * (c9 - 292)) / 0.300
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
                if 0 <= num and num >54:
                    return AQI_CALCULATION(0, 50, 0, 53, num)
                elif 54 <= num and num > 101:
                    return AQI_CALCULATION(51, 100, 54, 100, num)
                elif 101 <= num and num >361:
                    return AQI_CALCULATION(101, 150, 101, 300, num)
                elif 361 <= num and num > 650:
                    return AQI_CALCULATION(151, 200, 301, 649, num)
                elif 650 <= num and num > 1250:
                    return AQI_CALCULATION(201, 300, 650, 1249, num)
                elif 1250 <= num and num > 1650:
                    return AQI_CALCULATION(301, 400, 1250, 1649, num)
                elif 1650 <= num and num > 2050:
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
            print("AQI_PM25: {}".format(AQI_PM25))


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
'''
from btserver import BTServer
from bterror import BTError
from neo import Gpio

import argparse
import asyncore
import json
from threading import Thread
from time import sleep, time
from datetime import datetime
from json import dumps
import logging

# ------------ Alpha sense data sheet -------------
NO2_WE = 220; NO2_AE = 260; NO2_alpha = 0.207;
O3_WE = 414; O3_AE = 400; O3_alpha = 0.256;
CO_WE = 346; CO_AE = 274; CO_alpha = 0.276;
SO2_WE = 300; SO2_AE = 394; SO2_alpha = 0.300;
# ------------------------------------------------

def contol_mux(a, b, c, d):  # use binary bit to control mux
    neo.digitalWrite(gpiopins[0], d)
    neo.digitalWrite(gpiopins[1], c)
    neo.digitalWrite(gpiopins[2], b)
    neo.digitalWrite(gpiopins[3], a)
    raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
    scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
    return raw, scale

# ---------------------------N table -------------------------------------
# array for calculate alph
# temp              -30,  -20   -10     0    10     20   30    40    50
# index               0,    1,    2,    3,    4,    5,    6,    7 ,   8
NO2_tempArray = [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00, 2.70]  # SN1
O3_tempArray = [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 2.87]  # SN2
CO_tempArray = [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48, -0.80]  # SN3
SO2_tempArray = [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 1.95]  # SN4
# ------------------------------------------------------------------------

def get_n(temper, air):  # air = (NO2,O3, CO, SO2)
    # temper
    i = 0  # index
    mulx = 0  # multiple #times
    if (-30 <= temper < -20):
        i = 0;
        mulx = temper + 30  # ex -28'C + 30 = 2 >> 2
    elif (-20 <= temper < -10):
        i = 1;
        mulx = temper + 20
    elif (-10 <= temper < 0):
        i = 2;
        mulx = temper + 10
    elif (0 <= temper < 10):
        i = 3;
        mulx = temper
    elif (10 <= temper < 20):
        i = 4;
        mulx = temper - 10
    elif (20 <= temper < 30):
        i = 5;
        mulx = temper - 20
    elif (30 <= temper < 40):
        i = 6;
        mulx = temper - 30
    elif (40 <= temper < 50):
        i = 7;
        mulx = temper - 40
    elif (50 <= temper):
        i = 8;  # if temperature exceed 50 just give 50'C data

    N = 0.0
    if (air == 'O3'):
        if (i == 8):
            N = O3_tempArray[i]
        else:
            tmp = (O3_tempArray[i + 1] - O3_tempArray[i]) / 10.0
            N = O3_tempArray[i] + (tmp * mulx)

    elif (air == 'CO'):
        if (i == 8):
            N = CO_tempArray[i]
        else:
            tmp = (CO_tempArray[i + 1] - CO_tempArray[i]) / 10.0
            N = CO_tempArray[i] + (tmp * mulx)

    elif (air == 'NO2'):
        if (i == 8):
            N = NO2_tempArray[i]
        else:
            tmp = (NO2_tempArray[i + 1] - NO2_tempArray[i]) / 10.0
            N = NO2_tempArray[i] + (tmp * mulx)

    elif (air == 'SO2'):
        if (i == 8):
            N = SO2_tempArray[i]
        else:
            tmp = (SO2_tempArray[i + 1] - SO2_tempArray[i]) / 10.0
            N = SO2_tempArray[i] + (tmp * mulx)

    return N

# --------------------------- AQI table ----------------------------------------
# AQI              0-50,  51-100, 101-150, 151-200, 201-300, 301-400, 401-500
# index               0,       1,       2,       3,       4,       5,       6,
# MAX (03, PM25, CO, SO2, NO2, AQI)
O3_AqiArray = [55.0, 71.0, 86.0, 106.0, 200.0, 0.0, 0.0]
PM25_MaxAqiArray = [12.1, 35.5, 55.5, 150.5, 250.5, 350.5, 500.4]
CO_MaxAqiArray = [4.5, 9.5, 12.5, 15.5, 30.5, 40.5, 50.4]
SO2_MaxAqiArray = [36.0, 76.0, 186.0, 305.0, 605.0, 805.0, 1004.0]
NO2_MaxAqiArray = [54.0, 101.0, 361.0, 650.0, 1250.0, 1650.0, 2049.0]
Aqi_MaxAqiArray = [51.0, 101.0, 151.0, 201.0, 301.0, 401.0, 500.0]

# MIN (03, PM25, CO, SO2, NO2, AQI)
O3_AqiArray = [0.0, 55.0, 71.0, 86.0, 106.0, 0.0, 0.0]
PM25_MinAqiArray = [0.0, 12.1, 35.5, 55.5, 150.5, 250.5, 350.5]
CO_MinAqiArray = [0.0, 4.5, 9.5, 12.5, 15.5, 30.5, 40.5]
SO2_MinAqiArray = [0.0, 36.0, 76.0, 186.0, 305.0, 605.0, 805.0]
NO2_MinAqiArray = [0.0, 54.0, 101.0, 361.0, 650.0, 1250.0, 1650.0]
Aqi_MinAqiArray = [0.0, 51.0, 101.0, 151.0, 201.0, 301.0, 401.0]
# -------------------------------------------------------------------------------


def AQI_convert(c, air):
    c_low = 0.0
    c_high = 0.0
    i_low = 0.0
    i_high = 0.0
    I = 0.0

    if (air == 'PM25'):
        for i in range(0, 7):
            if (PM25_MaxAqiArray[6] < c):
                I = 500
                break;

            elif (PM25_MinAqiArray[i] <= c < PM25_MaxAqiArray[i]):
                c_low = PM25_MinAqiArray[i];
                c_high = PM25_MaxAqiArray[i];
                i_low = Aqi_MinAqiArray[i];
                i_high = Aqi_MaxAqiArray[i];
                break;

    elif (air == 'CO'):
        for i in range(0, 7):
            if (CO_MaxAqiArray[6] < c):
                I = 500
                break;

            elif (CO_MinAqiArray[i] <= c < CO_MaxAqiArray[i]):
                c_low = CO_MinAqiArray[i];
                c_high = CO_MaxAqiArray[i];
                i_low = Aqi_MinAqiArray[i];
                i_high = Aqi_MaxAqiArray[i];
                break;
    elif (air == 'SO2'):
        for i in range(0, 7):
            if (SO2_MaxAqiArray[6] < c):
                I = 500
                break;

            elif (SO2_MinAqiArray[i] <= c < SO2_MaxAqiArray[i]):
                c_low = SO2_MinAqiArray[i];
                c_high = SO2_MaxAqiArray[i];
                i_low = Aqi_MinAqiArray[i];
                i_high = Aqi_MaxAqiArray[i];
                break;
    elif (air == 'NO2'):
        for i in range(0, 7):
            if (NO2_MaxAqiArray[6] < c):
                I = 500
                break;

            if (NO2_MinAqiArray[i] <= c < NO2_MaxAqiArray[i]):
                c_low = NO2_MinAqiArray[i];
                c_high = NO2_MaxAqiArray[i];
                i_low = Aqi_MinAqiArray[i];
                i_high = Aqi_MaxAqiArray[i];
                break;
    elif (air == 'O3'):
        for i in range(0, 5):
            if (O3_AqiArray[4] < c):
                I = 500
                break;

            if (O3_AqiArray[i] <= c < O3_AqiArray[i]):
                c_low = O3_AqiArray[i];
                c_high = O3_AqiArray[i];
                i_low = Aqi_MinAqiArray[i];
                i_high = Aqi_MaxAqiArray[i];
                break;
    # AQI equation
    if (I != 500):
        I = (((i_high - i_low) / (c_high - c_low)) * (c - c_low)) + i_low

    return I;

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

    # epochtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #(int)(time())

    neo = Gpio()

    # S0 = 24 # pin to use
    # S1 = 25
    # S2 = 26
    # S3 = 27
    gpiopins = [24, 25, 26, 27]
    gpio = Gpio()

    pinnum = [0, 0, 0, 0]

    # Set GPIO pins to output
    # try:
    #   for pin in gpiopins:
    #       gpio.pinMode(pin, gpio.OUTPUT)
    # except Exception as e:
    #    logger.error("Error : GPIO pin {} .reason {}".format(pin, e.message))

    # Blink example
    for i in range(4):
        neo.pinMode(gpiopins[i], neo.OUTPUT)
    #temp=0
    #SN1=0
    #SN2=0
    #SN3=0
    #SN4=0
    #PM25=0

    while True:
        for client_handler in server.active_client_handlers.copy():

            # c0 temperature
            temp
            raw, scale = contol_mux(0, 0, 0, 0)
            sleep(1)
            v = raw * scale
            temp = (v - 500) / 10 - 6
            temp = (temp * 1.8) + 32
            print("temp: {} F".format(temp))

            # C2 NO2_we
            raw, scale = contol_mux(0, 0, 1, 0)
            sleep(0.05)
            c2 = raw * scale

            # C3 NO2_ae
            raw, scale = contol_mux(0, 0, 1, 1)
            sleep(0.05)
            c3 = raw * scale

            # SN1 NO2
            SN1 = ((c2 - NO2_WE) - (get_n(temp, 'NO2') * (c3 - NO2_AE))) / NO2_alpha
            SN1 = SN1 if (SN1 >= 0) else -SN1
            print("NO2 _SN1 : {}".format(SN1))

            # C4 O3_we
            raw, scale = contol_mux(0, 1, 0, 0)
            sleep(0.05)
            c4 = raw * scale

            # C5 O3_ae
            raw, scale = contol_mux(0, 1, 0, 1)
            sleep(0.05)
            c5 = raw * scale

            # SN2 O3
            SN2 = ((c4 - O3_WE) - (get_n(temp, 'O3') * (c5 - O3_AE))) / O3_alpha
            SN2 = SN2 if (SN2 >= 0) else -SN2
            print("O3 _SN2 : {}".format(SN2))

            # C6 CO_wE
            raw, scale = contol_mux(0, 1, 1, 0)
            sleep(0.05)
            c6 = raw * scale

            # C7 CO_aE
            raw, scale = contol_mux(0, 1, 1, 1)
            sleep(0.05)
            c7 = raw * scale

            # SN3 CO
            SN3 = ((c6 - CO_WE) - (get_n(temp, 'CO') * (c7 - CO_AE))) / CO_alpha
            SN3 = SN3 / 1000
            SN3 = SN3 if (SN3 >= 0) else -SN3
            print("CO_SN3 : {}".format(SN3))

            # C8 SO2_we
            raw, scale = contol_mux(1, 0, 0, 0)
            sleep(0.05)
            c8 = raw * scale

            # C9 SO2_aE
            raw, scale = contol_mux(1, 0, 0, 1)
            sleep(0.05)
            c9 = raw * scale

            # SN4 SO2
            SN4 = ((c8 - SO2_WE) - (get_n(temp, 'SO2') * (c9 - SO2_AE))) / SO2_alpha
            SN4 = SN4 if (SN4 >= 0) else -SN4
            print("SO2_SN4 : {}".format(SN4))

            # c11 PM2.5
            raw, scale = contol_mux(1, 0, 1, 1)
            sleep(0.05)
            c11 = (raw * scale) / 1000

            # PM2.5 equation

            hppcf = (240.0 * pow(c11, 6) - 2491.3 * pow(c11, 5) + 9448.7 * pow(c11, 4) - 14840.0 * pow(c11,3) + 10684.0 * pow(c11, 2) + 2211.8 * c11 + 7.9623)
            PM25 = 0.518 + .00274 * hppcf
            AQI_PM25 = AQI_convert(PM25, 'PM25')
            print("PM25 : {}".format(PM25))
            print("\n")

            AQI_NO2 = AQI_convert(SN1, 'NO2')
            AQI_O3 = AQI_convert(SN2, 'O3')
            AQI_CO = AQI_convert(SN3, 'CO')
            AQI_SO2 = AQI_convert(SN4, 'SO2')

            print("AQI_NO2:{} ".format(int(AQI_NO2)))
            print("AQI_O3:{}".format(int(AQI_O3)))
            print("AQI_CO:{}".format(int(AQI_CO)))
            print("AQI_SO2 : {}".format(int(AQI_SO2)))
            print("AQI_PM25: {}".format(int(AQI_PM25)))

        epochtime = datetime.now()
        nowtime = datetime.now()

        if args.output_format == "json":
            output = {
                "year": nowtime.year,
                "month": nowtime.month,
                "day": nowtime.day,
                "hour": nowtime.hour,
                "minute": nowtime.minute,
                "second": nowtime.second,
                'temp': temp,  # real temperature
                'SN1': SN1,  # NO2
                'SN2': SN2,  # O3
                'SN3': SN3,  # CO
                'SN4': SN4,  # SO2
                'PM25': PM25,
                'A_SN1':AQI_NO2,
                'A_SN2': AQI_O3,
                'A_SN3': AQI_CO,
                'A_SN4': AQI_SO2,
                'A_PM25':AQI_PM25
            }

            msg = json.dumps(output)
        elif args.output_format == "csv":
            msg = "Time:{}, {}, {}, {}, {}, {}, {}, {} ,{}, {}, {}  ".format(datetime, SN1, SN2, SN3, SN4, AQI_PM25, AQI_NO2, AQI_O3, AQI_CO,AQI_SO2, AQI_PM25)
        try:
            client_handler.send((msg + '\n').encode('ascii'))
        except Exception as e:
            BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
            client_handler.handle_close()

        # Sleep for 5 seconds
        sleep(2.5)
