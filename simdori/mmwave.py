#!/usr/bin/env python3

import pymysql # pymysql 임포트
import serial
import time
import binascii
import os
import getmac
import numpy as np
import random
from datetime import datetime

configFileName = '/home/pi/mmwave/xwr6843_vitalsigns.cfg' #configure file location
CLIport = {}
Dataport = {}
online = True

mac_address = getmac.get_mac_address()
print(f"MAC Address: {mac_address}")

tlv_index = [
[0  , 16],[16 , 24],[24 , 32],[32 , 40],[40 , 48], [48 , 56],[56 , 64],[64 , 72],[72 , 80],[80 , 88],
[88 , 96],[96 ,100],[100,104],[104,112],[112,120], [120,124],[124,128],[128,136],[136,144],[144,152],
[152,160],[160,168],[168,176],[176,184],[184,192], [192,200],[200,208],[208,216],[216,224],[224,232],
[232,240],[240,248],[248,256],[256,264],[264,272], [272,280],[280,288],[288,296],[296,304],[304,312],
[312,320],[320,328],[328,336],[336,344],[344,352], [352,360],[360,368],[368,-1]]

tlv_name = ["Magic_Number","version","TotalPacketLen","platform","fameNumber","timeCpuCycle","numDetectedObj","numTLVs",
"subFrameNumber","TLVtype","TLVlength","rangeBinIndexMax","rangeBinIndexPhase","maxVal","processingCyclesOut",
"rangeBinStratIndex","rangeBinEndIndex","unwrapPhasePeak_mm","outputFilterBreathOut","outputFilterHreatOut",
"heartRateEst_FFT","heartRateEst_FFT_4hz","heartRateEst_xCorr","heartReatEst_peakCount","breathingRateEst_FFT",
"breathingRateEst_xCorr","breathingRateEst_peakCount","confidenceMetricBreathOut","confidenceMetricBreathOut_xCorr",
"confidenceMetricHeartOut","confidenceMetricHeartOut_4Hz","confidenceMetricHeartOut_xCorr",
"sumEnergyBreathWfm","sumEnergyHeartWfm","motionDetectedFlag","BreathingRate_HarmEnergy","HeartRate_HarmEnergy",
"reserved7","reserved8","reserved9","reserved10","reserved11","reserved12","reserved13","reserved14","TLVtype","TLVlength","RangeProfile"]

mqtt_parm = ["now","fameNumber","rangeBinIndexPhase","unwrapPhasePeak_mm","outputFilterBreathOut","outputFilterHreatOut",
"heartRateEst_FFT","heartRateEst_FFT_4hz","heartRateEst_xCorr","heartReatEst_peakCount","breathingRateEst_FFT",
"breathingRateEst_xCorr","breathingRateEst_peakCount","confidenceMetricBreathOut","confidenceMetricBreathOut_xCorr",
"confidenceMetricHeartOut","confidenceMetricHeartOut_4Hz","confidenceMetricHeartOut_xCorr",
"sumEnergyBreathWfm","sumEnergyHeartWfm","motionDetectedFlag","BreathingRate_HarmEnergy","HeartRate_HarmEnergy",
"reserved7","reserved8","reserved9","reserved10","reserved11","reserved12","reserved13","reserved14","Real_value","Imaginary_value"]
# ------------------------------------------------------------------

# Function to configure the serial ports and send the data from
# the configuration file to the radar
def serialConfig(configFileName):

    global CLIport
    global Dataport
    # Open the serial ports for the configuration and the data ports

    # Raspberry pi
    print("USB port check!")
    file_list = os.listdir("/dev/")
    file_list_usb = [file for file in file_list if file.startswith('ttyUSB')]
    file_list_usb.sort()
    CLIport_path = file_list_usb[0]
    Dataport_path = file_list_usb[1]
    print(f"\nUSB port connect! {CLIport_path} {Dataport_path}")

    CLIport = serial.Serial(f"/dev/{CLIport_path}", 115200) #USB location, baud rate
    Dataport = serial.Serial(f"/dev/{Dataport_path}", 921600) #USB location, baud rate

    # Windows
    #CLIport = serial.Serial('COM3', 115200)
    #Dataport = serial.Serial('COM4', 921600)

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        CLIport.write((i+'\n').encode())
        print(i)
        time.sleep(0.01)

    return CLIport, Dataport

# ------------------------------------------------------------------

# Function to parse the data inside the configuration file
def parseConfigFile(configFileName):
    configParameters = {} # Initialize an empty dictionary to store the configuration parameters

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:

        # Split the line
        splitWords = i.split(" ")

        # Hard code the number of antennas, change if other configuration is used
        numRxAnt = 4
        numTxAnt = 2

        # Get the information about the profile configuration
        if "profileCfg" in splitWords[0]:
            startFreq = int(float(splitWords[2]))
            idleTime = int(splitWords[3])
            rampEndTime = float(splitWords[5])
            freqSlopeConst = float(splitWords[8])
            numAdcSamples = int(splitWords[10])
            numAdcSamplesRoundTo2 = 1;
            while numAdcSamples > numAdcSamplesRoundTo2:
                numAdcSamplesRoundTo2 = numAdcSamplesRoundTo2 * 2;
            digOutSampleRate = int(splitWords[11]);
        # Get the information about the frame configuration
        elif "frameCfg" in splitWords[0]:
            chirpStartIdx = int(splitWords[1]);
            chirpEndIdx = int(splitWords[2]);
            numLoops = int(splitWords[3]);
            numFrames = int(splitWords[4]);
            framePeriodicity = int(splitWords[5]);
        elif "vitalSignsCfg" in splitWords[0]:
            binStartIdx = int(float(splitWords[1]) / 0.0360577);
            binEndIdx = int(float(splitWords[2]) / 0.0360577);

    # Combine the read data to obtain the configuration parameters
    numChirpsPerFrame = (chirpEndIdx - chirpStartIdx + 1) * numLoops
    configParameters["numDopplerBins"] = numChirpsPerFrame / numTxAnt
    configParameters["numRangeBins"] = numAdcSamplesRoundTo2
    configParameters["rangeResolutionMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * numAdcSamples)
    configParameters["rangeIdxToMeters"] = (3e8 * digOutSampleRate * 1e3) / (2 * freqSlopeConst * 1e12 * configParameters["numRangeBins"])
    configParameters["dopplerResolutionMps"] = 3e8 / (2 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * configParameters["numDopplerBins"] * numTxAnt)
    configParameters["maxRange"] = (300 * 0.9 * digOutSampleRate)/(2 * freqSlopeConst * 1e3)
    configParameters["maxVelocity"] = 3e8 / (4 * startFreq * 1e9 * (idleTime + rampEndTime) * 1e-6 * numTxAnt)

    configParameters["startbinindex"] = binStartIdx
    configParameters["endbinindex"] = binEndIdx
    configParameters["numObservingRangeBins"] = binEndIdx - binStartIdx + 1

    configParameters["numRangeBinProcessed"] = 18.92
    return configParameters

# -------------------------    DATA PARSE   -----------------------------------------

def intType(buffer):
    temp = reverseHex(buffer)
    return int(temp, 16)

def reverseHex(buffer):
    output = ""
    for i in np.arange(len(buffer), 0, -2):
        output += buffer[i-2:i]
    return output


strData = ""
local_frame_index = 0
iteration_count = 0
def readData():
    global strData, local_frame_index, iteration_count, index, sensor_state
    if type(Dataport) == dict:
        local_frame_index = 0
        iteration_count = 0
        sensor_state = False
    elif type(Dataport) == serial.serialposix.Serial:
        readBuffer = Dataport.read(Dataport.in_waiting)
        strData += binascii.hexlify(readBuffer).decode('utf-8')
        if strData[0:16] == '0201040306050807':
            local_frame_index += 1
            total_length = intType(strData[24:32]) * 2
            frame_index = intType(strData[40:48])
            actual_length = len(strData)
            if total_length > actual_length:
                return

            now_obj = datetime.now()
            now_str = str(now_obj)
            print(frame_index, now_str)

            log_write(f"/home/pi/log/log_{now_obj.strftime('%Y%m%d%H0000')}.csv", f"{now_str},{strData[:total_length]}\n")

            tlv_hex = {}
            for i, index in enumerate(tlv_index):
                tlv_hex[tlv_name[i]] = strData[index[0]:index[1]]

            start_bin = intType(tlv_hex['rangeBinIndexPhase'])
            selected_bin = intType(tlv_hex['rangeBinEndIndex'])
            bin_index = selected_bin - start_bin

            message = f"REQUEST/4/"
            for key in tlv_hex:
                if key in mqtt_parm:
                    message += f"0x{reverseHex(tlv_hex[key])},"
            bin_q = reverseHex(tlv_hex['RangeProfile'][bin_index*4:bin_index*4+4])
            bin_i = reverseHex(tlv_hex['RangeProfile'][bin_index*4+4:bin_index*4+8])
            message += f"0x{bin_q},0x{bin_i}/{now_str}"
            mqtt_publish(mqtt_client, topic, message, set_max=1)

            if total_length < actual_length:
                strData = strData[total_length:]
            else:
                strData = ""
        else:
            strData = ""

        if iteration_count > 300:
            iteration_count = 0
            local_frame_index = 0
        else:
            iteration_count += 1

def log_write(log_file_name, text):
    f = open(f"{log_file_name}", 'a')
    f.write(text)
    f.close()

# -------------------------    MQTT   -----------------------------------------

from mqtt import mqtt_publish, mqtt_disconnect, mqtt_connect
sensor_state = False
def on_message(client, userdata, msg):
    global CLIport, Dataport, configParameters, sensor_state

    message = str(msg.payload.decode("utf-8"))
    # print(message)

    if message == "response/sensor_start":
        print(message)
        # Configurate the serial port
        if not(sensor_state):
            CLIport, Dataport = serialConfig(configFileName)
            configParameters = parseConfigFile(configFileName)
            sensor_state = True
    elif message == "response/sensor_stop":
        print(message)
        if sensor_state:
            CLIport.write(('sensorStop\n').encode())
            CLIport.close()
            Dataport.close()
            sensor_state = False

            CLIport = {}
            Dataport = {}
    elif message == "response/sensor_backup":
        # os.system('cmd /k "scp /home/pi/log/* simdori@simdori.com:/home/simdori/log/"')
        # os.system('cmd /k "sshpass -p "tlaehfl1!" scp /home/pi/log/* simdori@simdori.com:/home/simdori/log/"')
        pass

# -------------------------    MAIN   -----------------------------------------

if __name__ == "__main__":
    print('MMWAVE connected!')

    # Main loop
    host          = "mqtt.simdori.com"
    port          = 8883
    MQTT_HOST     = "mqtt.simdori.com"
    client_id     = f"mqttclient_server.js_{random.randrange(0,1000)}_sensor"
    user_name     = "simdori"
    password      = "simdori1!"
    clean_session = True
    topic = f"sensordata/{mac_address}"
    print(topic)

    mqtt_client = mqtt_connect(host, port, MQTT_HOST, client_id, user_name, password, 60, topic, clean_session=clean_session, on_message=on_message)
   # will set by ksjung20210317
    lwm="mmwave Gone Offline" # Last will message
    print("Setting Last will message=",lwm,"topic is",topic )
    mqtt_client.will_set(topic,lwm,1,retain=False)

    while True:
        try:
            readData()
            time.sleep(0.01)
        except KeyboardInterrupt:
            CLIport.write(('sensorStop\n').encode())
            CLIport.close()
            Dataport.close()
            mqtt_disconnect(mqtt_client)
            break
        except Exception as e:
            print(e)
            CLIport.write(('sensorStop\n').encode())
            CLIport.close()
            Dataport.close()
            mqtt_disconnect(mqtt_client)
            break
