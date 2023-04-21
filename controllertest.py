import turtle
import math
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

joystick = turtle.Turtle()
joystick.shape("circle")
joystick.color("blue")
joystick.penup()

wn = turtle.Screen()
wn.tracer(0)

square = 200
def move_turtle(x,y):
    if x > square/2 or x < square/2*-1:
        if y > square/2:
            print()
        else:
            joystick.setpos(joystick.xcor(), y)
    elif y > square/2 or y < square/2*-1:
        if x > square/2:
            print()
        else:
            joystick.setpos(x, joystick.ycor())
    else:
        joystick.setpos(x,y)


def calaclations():
    x = joystick.xcor()
    y = joystick.ycor()
    #A, D equation: sin(angle+1/4pi)*mag
    #B, C equation: sin(angle-1/4pi)*mag
    angle =  math.atan2(y, x)
    mag = math.sqrt(x**2 + y**2)
    pi = math.pi
    change = 1.3
    out1 = math.sin(angle+(pi/4))*mag * change
    out2 = math.sin(angle-(pi/4))*mag * change
    print(out1, out2)
    ser.write(b"{}, {}\n".format(out1, out2))

def setup():
    pen = turtle.Turtle()
    pen.penup()
    pen.speed(0)
    pen.setpos(0, (square/2)*-1)
    pen.pendown()
    pen.fd(square/2)
    for n in range(3):
        pen.lt(90)
        pen.fd(square)
    pen.lt(90)
    pen.fd(square/2)

setup()


joystick.ondrag(move_turtle)
while True:
    wn.update()
    calaclations()
