import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False) #turn off warnings

#channels = [35, 37] #what channels are being used
# pin = [37, 38, 31, 29, 23, 21, 19, 7, 32]

AIN1 = 35
AIN2 = 37

PWMB = 32
PWMA = 33


pins = [AIN1, AIN2, PWMA]

GPIO.setup(pins, GPIO.OUT) #make those channels outputs


# GPIO.setup(PWMA, GPIO.OUT)



''' 
32 and 33 are pwm pins (probably)

set all pins to output

FOR POSITIVE SPEED:
pin1 = high
pin2 = low

write pwm that is |speed|
FOR NEGATIVE SPEED:
pin1 = low
pin2 = high
'''
H = GPIO.HIGH
L = GPIO.LOW

# def motorWrite(speed, pin_IN1, pin_IN2, pin_pwm):
#     if speed < 0: #controll the direction of the motors
#         GPIO.output(pin_IN1, HIGH) #set in1 to high
#         GPIO.output(pin_IN2, LOW) #set in2 to low
#     else:
#         GPIO.output(pin_IN1, LOW) #set in1 to low
#         GPIO.output(pin_IN2, HIGH) #set in2 to high
#     GPIO.PWM(pin_pwm, abs(speed))


while True:
    GPIO.output(pins, H)
    time.sleep(.01)
    GPIO.output(pins, L)
    time.sleep(.02)
    # motorWrite(50, AIN1, AIN2, PWMA)
    # time.sleep(5)
    # motorWrite(-50, AIN1, AIN2, PWMA)
    # time.sleep(8)