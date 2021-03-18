import os
import serial

# Raspberry pi
print("USB port check!")
file_list = os.listdir("/dev/")
file_list_usb = [file for file in file_list if file.startswith('ttyUSB')]
file_list_usb.sort()
CLIport_path = file_list_usb[0]
Dataport_path = file_list_usb[1]
print(f"\nUSB port connect! {CLIport_path} {Dataport_path}")

CLIport = serial.Serial(f"/dev/{CLIport_path}", 115200) #USB location, baud rate
# Dataport = serial.Serial(f"/dev/{Dataport_path}", 921600) #USB location, baud rate
CLIport.write(('sensorStop\n').encode())
CLIport.close()
