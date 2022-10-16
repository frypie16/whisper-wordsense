# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:17:11 2022

@author: fahad
"""
import serial

class Controller:
    def __init__(self, com):
        self.isConnected = False
        self.motorPins = [2,3,4,5,6,7]
        self.CONN_FLAG = 0x32
        self.FRAME_START = 0x06
        self.SETNAME = 0x07
        self.BAUDRATE = 9600
        self.direction_codes = {0x23:0,
                                0x24:1,
                                0x25:2,
                                0x26:3,
                                0x27:4,
                                0x28:5}
        self.emotion_codes = {0x12: "neutral",
                              0x10: "positive",
                              0x11: "negative"}
        self.port = serial.Serial(com, self.BAUDRATE)
        print("arduino powered on")
        while self.isConnected is False:
            if self.port.in_waiting == 0:
                continue
            print(self.port.read())
            if self.port.read() != self.CONN_FLAG:
                continue
            self.port.write(self.CONN_FLAG)
            while self.port.in_waiting > 0:
                dummy = self.port.read()
            self.isConnected = True
            self.pwr = 1
            print("controller connected. activated pin 8")
    
    def loop(self):
        if self.port.in_waiting > 0:
            if self.read() != self.FRAME_START:
                return
            emotion = self.read()
            direction = self.read()
            print("activated motor pin {dPin}".format(dPin=self.motorPins[self.direction_codes[direction]]))
            print("activated emotion: {etype}".format(etype=self.emotion_codes[emotion]))
    
            