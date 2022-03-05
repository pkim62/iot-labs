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
        coo = 0

        try:
            while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    if data == b"temp\r\n":
                        print(data)
                        client.sendall(caroToString(coo).encode())
                    elif data == b"87\r\n":
                        coo = change_car(coo, 0)
                        client.sendall(caroToString(coo).encode())
                    elif data == b"83\r\n":
                        coo = change_car(coo, -2)
                        client.sendall(caroToString(coo).encode())
                    elif data == b"65\r\n":
                        coo = change_car(coo, 1)
                        client.sendall(caroToString(coo).encode())

                    elif data == b"68\r\n":
                        coo = change_car(coo,-1)
                        client.sendall(caroToString(coo).encode())
                    else:
                        print(data)
                        client.sendall(data) # Echo back to client
        except:
            print("Closing socket")
            client.close()
            s.close()
            fc.stop()

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

def change_car(car_o ,target):
  if target == car_o:
    return car_o
  elif target > car_o:
    go_left()
    car_o +=  1
    return change_car(car_o + 1, target)
  elif target < car_o:
    go_right()
    car_o -= 1
    return change_car(car_o - 1, target)

def caroToString(car_o):
    if car_o == 0:
        return "north"
    elif car_o == 1:
        return "west"
    elif car_o == -1:
        return "east"
    else:
        return "south"

def measure_temp():
    cpu = CPUTemperature()
    return str(cpu.temperature)

if __name__ == "__main__":
    main()
