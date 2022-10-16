# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 21:12:25 2022

@author: fahad
"""
import pyaudio as pa
import numpy as np
import keyboard
import serial
from scipy.io.wavfile import write
from controller import Controller
import threading

emotion_codes = [0x12, 0x10, 0x11]
direction_codes = [0x23, 0x24, 0x25, 0x26, 0x28, 0x29]

# defs
_CHUNKSIZE = 1024
_SQRT_CHUNKSIZE = 32
_SRATE = 44100
_THRESHOLD = 0.2
_RECORD_THRESHOLD = 50000
_PORT='COM1'
_BAUDRATE=9600
_FILENAME = 'record.wav'

_isRecording = False
_isConnected = False
_bufferdata = np.empty(1, dtype=np.int16)
_username = 'random'

p = pa.PyAudio()

#callback function to record the data given the audio is louder
#than a specified threshold 
def record(in_data, frame_count, time_info, status):
    global _bufferdata, _isRecording
    audio_data = np.fromstring(in_data, dtype=np.int16)
    rms = np.linalg.norm(audio_data) / 32
    if rms > _THRESHOLD:
        _bufferdata = np.r_[_bufferdata, audio_data]
        _isRecording = True
    else:
        _isRecording = False
    return (None, pa.paContinue)

def saveWAV():
    write(_FILENAME, _SRATE, _bufferdata)
    

stream = p.open(_SRATE, 
                2, 
                pa.paInt16, 
                input=True,
                output=False,
                frames_per_buffer=_CHUNKSIZE, 
                stream_callback=record)


_port = serial.Serial(_PORT, _BAUDRATE)

#sends data to the serial port. 
def sendHapticSignals(emotion, direction, text=None):
    payload = [0x06]
    payload.append(emotion_codes[emotion])
    payload.append(direction_codes[direction])
    if text is not None:
        for b in bytearray(text, 'ascii'):
            payload.append(b)
    payload.append(0x10)
    _port.write(payload)
    

def whisper():
    emotion = 0
    text = None #text can be none if transcript is not converted to haptics
    isNamePresent = False
    direction = 3
    #api calling stuff to do here
    return (emotion, text, direction, isNamePresent)

_isRunning = True

def endProgram():
    global _isRunning
    _isRunning = False

keyboard.add_hotkey('e', endProgram)
print('listening. press e to end program')

def arduinoThreadFunc():
    print("starting arduino...")
    arduino = Controller('COM2')
    while True:
        arduino.loop()

arduino_thread = threading.Thread(target=arduinoThreadFunc, daemon=True)
arduino_thread.start()
_port.write(0x32)

while _isRunning:
    if _isConnected is False:
        _port.write(0x32)
        if _port.in_waiting > 0:
            if _port.read() == 0x32:
                _isConnected = True
    if _isRecording is False:
        if len(_bufferdata) > _RECORD_THRESHOLD:
            saveWAV()
            emotion, text, direction, isNamePresent = whisper()
            sendHapticSignals(emotion, direction)
        _bufferdata = np.empty(1, dtype=np.int16)
    
_port.close()