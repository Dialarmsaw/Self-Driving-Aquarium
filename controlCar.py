import turtle
import math
import serial
import keyboard
import time

#Setup a serial (USB) communication with the arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

#Create the Screen for the controller
wn = turtle.Screen()
wn.tracer(0)

#Draw the box
def setup():
    pen = turtle.Turtle()
    pen.up()
    pen.goto(-125, -125)
    pen.down()
    for i in range(4):
        pen.fd(250)
        pen.lt(90)
    pen.hideturtle()

#Make the joystick
joystick = turtle.Turtle()
joystick.color("purple")
joystick.shape("circle")
joystick.penup()

#Make bounderies
def outOfBounds(x, y, bound):
    if x > bound/2 or x < bound/2*-1:
        if x < 0:
            joystick.goto(-151, y)
        else:
            joystick.goto(150, y)
    if y > bound/2 or y < bound/2*-1:
        if y < 0:
            joystick.goto(x, -150)
        else:
            joystick.goto(x, 150)

#Follow the mouse
def dragging(x, y):
    joystick.ondrag(None)
    joystick.goto(x, y)
    joystick.ondrag(dragging)

#Calculate the motor outputs
def calculations(x, y):
    if keyboard.is_pressed("q"):
        ser.write(b"0,0")
        time.sleep(5)

    #A, D equation: sin(angle+1/4pi)*mag
    #B, C equation: sin(angle-1/4pi)*mag
    angle =  math.atan2(y, x)
    mag = math.sqrt(x**2 + y**2)
    pi = math.pi
    out1 = math.sin(angle+(pi/4))*mag
    out2 = math.sin(angle-(pi/4))*mag
    if out1 < -0.708 and out2 > 212.84:
        out1 = -0.708
        out2 = 212.84
    if out2 > 0.708 and out1 < -212.84:
        out2 = 0.708
        out1 = -212.84
    print(out1, out2)
    ser.write(b"{}, {}\n".format(out1, out2))

setup()

turtle.listen()
joystick.ondrag(dragging)  # When we drag the controller object call dragging

while True:
    if keyboard.is_pressed("esc"):
        break
    outOfBounds(joystick.xcor(), joystick.ycor(), 300)
    wn.update()
    outOfBounds(joystick.xcor(), joystick.ycor(), 300)
    calculations(joystick.xcor(), joystick.ycor())
    if keyboard.is_pressed("esc"):
        break
ser.write(b"0,0")
print("E Stopped!")