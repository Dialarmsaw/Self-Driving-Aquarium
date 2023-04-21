import serial
import time

'''
To find the port, go into terminal any type:
ls /dev/tty*
Then, put it in the serial.Serial command
'''

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

speed1 = 0
speed2 = 0



for i in range(100):
    ser.write(b"{}, {}\n".format(speed1, speed2)) #ALWAYS PUT A B AT THE BEGGINING TO CONVERT TO BYTES FOR SERIAL
    print("sent")
    speed1 += 1
    speed2 += 1
    time.sleep(1)