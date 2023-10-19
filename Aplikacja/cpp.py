#Constant power panning
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from IPython.display import Audio
from numpy.fft import fft, ifft
import wave
from scipy import signal

import panning


def changeVolume(signal, mod):
    return (signal * pow(2, (np.sqrt(np.sqrt(np.sqrt(mod))) * 192 - 192)/6)).astype(np.int16)

def loadSignal(filename):
    obj = wave.open(filename, "rb")
    fr = np.frombuffer(obj.readframes(-1), dtype=np.int16)
    return fr, obj

def saveSignal(obj, left, right, filename):
    framerate = obj.getframerate()
    sampwidth=obj.getsampwidth()
    signal = np.insert(right, np.arange(len(left)), left)
    nchannels = 2
    obj_new = wave.open(filename, "wb")
    obj_new.setnchannels(nchannels)
    obj_new.setsampwidth(sampwidth)
    obj_new.setframerate(framerate)
    obj_new.writeframes(signal)

def modify(angle=None, verbose=True):
    aoa = np.pi/6
    Pan = True

    if(angle == None):
        angle = np.pi/2
        angle = np.pi/2 + angle 
    output = "../Audio/output.wav"

    fr, obj = loadSignal("../Audio/speech.wav")
    nchannels = obj.getnchannels()
    if nchannels > 1:
        left = fr[1::2]
        right = fr[::2]
    else:
        left = right = fr

    if Pan:
        if verbose:
            print(f"Obrót wynosi {np.rad2deg(angle)} stopni licząc zgodnie z ruchem wskazówek zegara od godziny 9")
        left, right = panning.ConstantPowerPan(angle,left,right)
       #left, right = pan(angle,left,right)
    

    signal = np.insert(right, np.arange(len(left)), left)
    saveSignal(obj, left, right, output)
    return signal, Audio(filename=output)

'''
def pan(angle, left, right):
    angle = angle/2
    rightAmpMod = np.sin(angle)
    leftAmpMod = np.cos(angle)
    left = changeVolume(left, leftAmpMod)
    right = changeVolume(right, rightAmpMod)
    return left, right
'''

def audio8d():
    fr, obj = loadSignal("../Audio/speech.wav")
    nchannels = obj.getnchannels()
    if nchannels > 1:
        left = fr[1::2]
        right = fr[::2]
    else:
        left = right = fr

    rot_seconds = 8
    framerate = obj.getframerate()
    nframes = len(fr)

    angles = np.arange(0, np.pi, np.pi*5/180)
    angles = np.concatenate((angles, np.flip(angles)))
    print(angles)
    print(len(angles))

    


    window = int(rot_seconds * framerate / len(angles))

    repeats = int(np.ceil(nframes/framerate/rot_seconds))
    angles = np.tile(angles, repeats)
    print(f"Powtarzanie {repeats} razy")

    left = left.copy()
    right = right.copy()

    for i in range(0, len(angles)):
        print(i*window, (i+1)*window)
        left[i*window:(i+1)*window], right[i*window:(i+1)*window] = panning.ConstantPowerPan(angles[i], left[i*window:(i+1)*window], right[i*window:(i+1)*window])

    signal = np.insert(right, np.arange(len(left)), left)
    nchannels = 2
    output = "../Audio/8daudiooutput.wav"
    saveSignal(obj, left, right, output)
    return signal, Audio(filename=output)

