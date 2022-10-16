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

# defs
CHUNKSIZE = 1024
SQRT_CHUNKSIZE = 32
SRATE = 44100
THRESHOLD = 0.2
RECORD_THRESHOLD = 50000
PORT='COM1'
BAUDRATE=9600
FILENAME = 'record.wav'

_isRecording = False
_bufferdata = np.empty(1, dtype=np.int16)
_username = 'random'

p = pa.PyAudio()

#callback function to record the data given the audio is louder
#than a specified threshold 
def record(in_data, frame_count, time_info, status):
    global _bufferdata, _isRecording
    audio_data = np.fromstring(in_data, dtype=np.int16)
    rms = np.linalg.norm(audio_data) / 32
    if rms > THRESHOLD:
        _bufferdata = np.r_[_bufferdata, audio_data]
        _isRecording = True
    else:
        _isRecording = False
    return (None, pa.paContinue)

def saveWAV():
    write(FILENAME, SRATE, _bufferdata)
    

stream = p.open(SRATE, 
                2, 
                pa.paInt16, 
                input=True,
                output=False,
                frames_per_buffer=CHUNKSIZE, 
                stream_callback=record)

#uncomment this to enable serial port comms
#_port = serial.Serial(PORT, BAUDRATE)

#sends data to the serial port. 
def sendHapticSignals(emotion, text=None):
    payload = []
    #positive emotion
    if emotion == 1:
        payload.append(0x10)
    #negative emotion
    elif emotion == -1:
        payload.append(0x11)
    else:
        payload.append(0x12)

def whisper():
    emotion = 0
    text = None #text can be none if transcript is not converted to haptics
    isNamePresent = False
    #api calling stuff to do here
    return (emotion, text, isNamePresent)

_isRunning = True

def endProgram():
    global _isRunning
    _isRunning = False

keyboard.add_hotkey('e', endProgram)
print('listening. press e to end program')

while _isRunning:
    if _isRecording is False:
        if _bufferdata.length > RECORD_THRESHOLD:
            saveWAV()
            emotion = whisper()
        _bufferdata = np.empty(1, dtype=np.int16)
    
#uncomment this to enable serial port comms
#_port.close()