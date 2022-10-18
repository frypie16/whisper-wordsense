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
            if self.serRead() != self.CONN_FLAG:
                continue
            self.serWrite(self.CONN_FLAG)
            self.isConnected = True
            self.pwr = 1
            print("controller connected. activated pin 8")
            
    def serRead(self):
        return int.from_bytes(self.port.read(), 'big')
    
    def serWrite(self, x):
        self.port.write(x.to_bytes(1, 'big'))
    
    def loop(self):
        if self.port.in_waiting > 2:
            if self.serRead() != self.FRAME_START:
                return
            emotion = self.serRead()
            direction = self.serRead()
            print("activated motor pin {dPin}".format(dPin=self.motorPins[self.direction_codes[direction]]))
            print("activated emotion: {etype}".format(etype=self.emotion_codes[emotion]))
            
    def __del__(self):
        self.port.close()
        print("arduino powered down")
    
            