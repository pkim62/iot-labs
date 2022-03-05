import socket
from collections import defaultdict
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin
import time
import picar_4wd as fc
import random
import numpy as np
import sys
from gpiozero import CPUTemperature
def main():
    #got help from https://medium.com/@kevalpatel2106/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f
    HOST = "10.0.0.139" # IP address of your Raspberry PI
    PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        try:
            while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    if data == b"temp\r\n":
                        print(data)
                        client.sendall(measure_temp().encode())
                    elif data == b"87\r\n":
                    elif data == b"83\r\n":
                    elif data == b"65\r\n":
                    elif data == b"68\r\n":
                    else:
                        print(data)
                        client.sendall(data) # Echo back to client
        except:
            print("Closing socket")
            client.close()
            s.close()

def go_forth():
  fc.forward(10)
  time.sleep(.06)
  fc.stop()

def go_left():
  fc.turn_left(20)
  time.sleep(.95)
  fc.stop()

def go_right():
  fc.turn_right(20)
  time.sleep(.9)
  fc.stop()

def change_car(target):
  global car_o
  if target == car_o:
    return car_o
  elif target > car_o:
    go_left()
    car_o +=  1
    return change_car(target)
  elif target < car_o:
    go_right()
    car_o -= 1
    return change_car(target)

def measure_temp():
    cpu = CPUTemperature()
    return str(cpu.temperature)

if __name__ == "__main__":
    main()
