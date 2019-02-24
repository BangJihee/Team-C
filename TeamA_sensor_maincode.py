
from btserver import BTServer
from bterror import BTError

import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time
from neo import Gpio

########################### N table ###################################
#array for calculate alph
#temp              -30,  -20   -10     0    10     20   30    40    50
#index               0,    1,    2,    3,    4,    5,    6,    7 ,   8
O3_tempArray  = [ 0.18, 0.18, 0.18, 0.18, 0.18, 0.36, 0.76, 1.56, 2.87]
SO2_tempArray = [ 0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 1.95]
NO2_tempArray = [ 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00, 2.70]
CO_tempArray  = [ 1.40, 1.03, 0.85, 0.62, 0.30, 0.03,-0.25,-0.48,-0.80]
#######################################################################

def get_alpha(temper, air): #air = NO2,O3, CO, SO2
    i=0 #index
    mulx=0 # multiple #times
    if(-30<=temper<-20):
        i = 0
        mulx = temper + 30  # ex -28'C + 30 = 2 >> 2
    elif(-20<=temper<-10):
        i = 1
        mulx = temper + 20
    elif (-10 <= temper < 0):
        i = 2
        mulx = temper + 10
    elif (0 <= temper < 10):
        i = 3
        mulx = temper
    elif (10 <= temper < 20):
        i = 4
        mulx = temper -10
    elif (20 <= temper < 30):
        i = 5
        mulx = temper -20
    elif (30 <= temper < 40):
        i = 6
        mulx = temper -30
    elif (40 <= temper < 50):
        i = 7
        mulx = temper - 40
    elif (50 <= temper):
        i = 8 # if temperature exceed 50 just give 50'C data

    N =0.0
    if(air == 'O3'):
        if(i==8):
            N=O3_tempArray[i]
        else:
            tmp=( O3_tempArray[i + 1] - O3_tempArray[i] ) / 10.0
            N=O3_tempArray[i] + (tmp * mulx)

    elif(air == 'CO'):
        if(i==8):
            N=CO_tempArray[i]
        else:
            tmp=( CO_tempArray[i + 1] - CO_tempArray[i] ) / 10.0
            N=CO_tempArray[i] + (tmp * mulx)

    elif(air == 'NO2'):
        if(i==8):
            N=NO2_tempArray[i]
        else:
            tmp=( NO2_tempArray[i + 1] - NO2_tempArray[i] ) / 10.0
            N=NO2_tempArray[i] + (tmp * mulx)

    elif (air == 'SO2'):
        if(i==8):
            N=SO2_tempArray[i]
        else:
            tmp=( SO2_tempArray[i + 1] - SO2_tempArray[i] ) / 10.0
            N=SO2_tempArray[i] + (tmp * mulx)

    return N

SN1_Vpcbwe = 286
SN2_Vpcbwe = 417
SN3_Vpcbwe = 265
SN4_Vpcbwe = 275
SN1_Vpcbae = 292
SN2_Vpcbae = 402
SN3_Vpcbae = 281
SN4_Vpcbae = 295
SN1_sensitivity = 0.258
SN2_sensitivity = 0.393
SN3_sensitivity = 0.292
SN4_sensitivity = 0.288



############################ AQI table ##################################
#AQI              0-50,  51-100, 101-150, 151-200, 201-300, 301-400, 401-500
#index               0,       1,       2,       3,       4,       5,       6,
#MAX (038, O31, PM25, CO, SO2, NO2, AQI)
O3_8Max_AqiArray  = [55.0, 71.0, 86.0, 106.0, 200.0,  0.0,  0.0]
PM25_MaxAqiArray  = [12.1, 35.5, 55.5, 150.5, 250.5, 350.5, 500.4]
CO_MaxAqiArray    = [4.5, 9.5, 12.5, 15.5, 30.5, 40.5, 50.4]
SO2_MaxAqiArray   = [36.0, 76.0, 186.0, 305.0, 605.0, 805.0, 1004.0]
NO2_MaxAqiArray   = [54.0, 101.0, 361.0, 650.0, 1250.0, 1650.0, 2049.0]
Aqi_MaxAqiArray   = [51.0, 101.0, 151.0, 201.0, 301.0, 401.0, 500.0]

#MIN (038, O31, PM25, CO, SO2, NO2, AQI)
O3_8Min_AqiArray  = [0.0, 55.0, 71.0, 86.0, 106.0, 0.0, 0.0]
PM25_MinAqiArray  = [0.0, 12.1, 35.5, 55.5, 150.5, 250.5, 350.5]
CO_MinAqiArray    = [0.0, 4.5, 9.5, 12.5, 15.5, 30.5, 40.5]
SO2_MinAqiArray   = [0.0, 36.0, 76.0, 186.0, 305.0, 605.0, 805.0]
NO2_MinAqiArray   = [0.0, 54.0, 101.0, 361.0, 650.0, 1250.0, 1650.0]
Aqi_MinAqiArray   = [0.0, 51.0, 101.0, 151.0, 201.0, 301.0, 401.0]
#######################################################################


def AQI_convert( c , air):
    c_low = 0.0
    c_high = 0.0
    i_low = 0.0
    i_high = 0.0
    I = 0.0

    if (air == 'PM25'):
        for i in range(0, 7):
            if(PM25_MaxAqiArray[6] < c):
                I=500
                break

            elif ( PM25_MinAqiArray[i] <= c < PM25_MaxAqiArray[i] ):
                c_low = PM25_MinAqiArray[i]
                c_high = PM25_MaxAqiArray[i]
                i_low = Aqi_MinAqiArray[i]
                i_high = Aqi_MaxAqiArray[i]
                break

    elif (air == 'CO'):
        for i in range(0, 7):
            if (CO_MaxAqiArray[6] < c):
                I = 500
                break

            elif ( CO_MinAqiArray[i] <= c < CO_MaxAqiArray[i] ):
                c_low = CO_MinAqiArray[i]
                c_high = CO_MaxAqiArray[i]
                i_low = Aqi_MinAqiArray[i]
                i_high = Aqi_MaxAqiArray[i]
                break
    elif (air == 'SO2'):
        for i in range(0, 7):
            if (SO2_MaxAqiArray[6] < c):
                I = 500
                break

            elif ( SO2_MinAqiArray[i] <= c < SO2_MaxAqiArray[i] ):
                c_low = SO2_MinAqiArray[i]
                c_high = SO2_MaxAqiArray[i]
                i_low = Aqi_MinAqiArray[i]
                i_high = Aqi_MaxAqiArray[i]
                break
    elif (air == 'NO2'):
        for i in range(0, 7):
            if (NO2_MaxAqiArray[6] < c):
                I = 500
                break

            if ( NO2_MinAqiArray[i] <= c < NO2_MaxAqiArray[i] ):
                c_low = NO2_MinAqiArray[i]
                c_high = NO2_MaxAqiArray[i]
                i_low = Aqi_MinAqiArray[i]
                i_high = Aqi_MaxAqiArray[i]
                break
    elif (air == 'O3'):
        for i in range(0, 5):
            if (O3_8Max_AqiArray[4] < c):
                I = 500
                break

            if ( O3_8Min_AqiArray[i] <= c < O3_8Max_AqiArray[i] ):
                c_low = O3_8Min_AqiArray[i]
                c_high = O3_8Max_AqiArray[i]
                i_low = Aqi_MinAqiArray[i]
                i_high = Aqi_MaxAqiArray[i]
                break
    ###################computing AQI formula####################
    if(I!=500):
        I = (((i_high - i_low) / (c_high - c_low)) * (c - c_low)) + i_low
    ############################################################

    return I


# get_alpha example
# get_alpha(50,'O3')


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

    while True:
        for client_handler in server.active_client_handlers.copy():
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"

            epoch_time = int(time())    # epoch time
            neo = Gpio()

            S0 = 2  # pin to use
            S1 = 3
            S2 = 4
            S3 = 5

            pinNum = [S0, S1, S2, S3]

            num = [0, 0, 0, 0]

            # Blink example
            for i in range(4):
                neo.pinMode(pinNum[i], neo.OUTPUT)


            #Temperature sensor
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)



            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c0 = raw * scale
            temp_celsius = (c0-500) / 10
            temp = (temp_celsius * 1.8) + 32
            temp = int(temp)



            #Alphasense SN1
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c2 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c3 = raw * scale

            SN1 = ((c2 - SN1_Vpcbwe) -(get_alpha(temp_celsius,'NO2'))*(c3 - SN1_Vpcbae)) / SN1_sensitivity
            SN1 = SN1 if (SN1 >= 0) else -SN1
            AQI_SN1 = AQI_convert(SN1, 'NO2')
            AQI_SN1 = int(AQI_SN1)

            #Alphasense SN2
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c4 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c5 = raw * scale

            SN2 = ((c4-SN2_Vpcbwe)- (get_alpha(temp_celsius,'O3'))*(c5-SN2_Vpcbae)) / SN2_sensitivity
            SN2 = SN2 if (SN2 >= 0) else -SN2
            AQI_SN2 = AQI_convert(SN2, 'O3')
            AQI_SN2 = int(AQI_SN2)

            #Alphasense SN3
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c6 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c7 = raw * scale

            SN3 = (((c6 -SN3_Vpcbwe)-(get_alpha(temp_celsius,'CO'))*(c7-SN3_Vpcbae)) / SN3_sensitivity)/1000
            SN3 = SN3 if (SN3 >= 0) else -SN3
            AQI_SN3 = AQI_convert(SN3, 'CO')
            AQI_SN3 = int(AQI_SN3)


            #Alphasense SN4
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c8 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c9 = raw * scale

            SN4 = ((c8 - SN4_Vpcbwe)-(get_alpha(temp_celsius,'SO2'))*(c9-SN4_Vpcbae)) / SN4_sensitivity
            SN4 = SN4 if (SN4 >= 0) else -SN4
            AQI_SN4 = AQI_convert(SN4, 'SO2')
            AQI_SN4 = int(AQI_SN4)


            #PM2.5
            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c11= (raw * scale) / 1000

            hppcf = (240.0 * pow(c11, 6) - 2491.3 * pow(c11, 5) + 9448.7 * pow(c11, 4) - 14840.0 * pow(c11, 3) + 10684.0 * pow(c11, 2) + 2211.8 * (c11) + 7.9623)
            PM25 = 0.518 + .00274 * hppcf
            AQI_PM25 = AQI_convert(PM25, 'PM25')
            AQI_PM25 = int(AQI_PM25)

            AQI_AVG = (AQI_SN1 + AQI_SN2 +AQI_SN3 + AQI_SN4 + AQI_PM25)/5
            AQI_AVG = int(AQI_AVG)


            msg = ""
            if args.output_format == "csv":
                msg = "realtime, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(epoch_time, temp, SN1, SN2, SN3, SN4, PM25, AQI_SN1, AQI_SN2, AQI_SN3, AQI_SN4, AQI_PM25, AQI_AVG)
            elif args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': temp,
                          'NO2_SN1': SN1,
                          'O3_SN2': SN2,
                          'CO_SN3': SN3,
                          'SO2_SN4': SN4,
                          'PM25': PM25,
                          'AQI_SN1': AQI_SN1,
                          'AQI_SN2': AQI_SN2,
                          'AQI_SN3': AQI_SN3,
                          'AQI_SN4': AQI_SN4,
                          'AQI_PM25': AQI_PM25}
                msg = json.dumps(output)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(2.5)

