import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from IPython.display import Audio
from numpy.fft import fft, ifft
import wave
from scipy import signal

global nchannels 

def changeVolume(sig, volumeFactor):
    multiplier = pow(2, (np.sqrt(np.sqrt(np.sqrt(volumeFactor))) * 192 - 192)/6)
    return np.round(sig * multiplier).astype(np.int16)

def addEcho(obj, sig, echoDelay, echoVolumeFactor):
    delayFrames = int(echoDelay*obj.getframerate())
    sigEcho = np.concatenate((sig[-delayFrames:],sig[:len(sig)-delayFrames]))
    sigEcho = np.concatenate((np.zeros(delayFrames), sig[:len(sig)-delayFrames]))
    sigEcho = changeVolume(sigEcho, echoVolumeFactor)
    return np.add(sig, sigEcho)

def muffle(obj, sig):
    #Experimental
    sos = signal.butter(10, 500, 'hp', fs=obj.getframerate(), output='sos')
    filtered = signal.sosfilt(sos, sig)
    filtered = np.round(filtered).astype(np.int16)
    return filtered

def muffleFft(obj, sig):
    fftfr = np.fft.rfft(sig)
    freq = np.fft.rfftfreq(len(sig), d=1./obj.getframerate())
    for i,val in enumerate(freq):
        if (val) < 500:
            fftfr[i] = 0
    return np.fft.irfft(fftfr).astype(np.int16)

def reverse(sig):
    return np.flip(sig)

def monoToStereo(sig):
    global nchannels
    nchannels = 2
    return np.repeat(sig,2)

def audio360(obj, sig):
    fr = sig.copy()

    if obj.getnchannels() < 2:
        fr = monoToStereo(fr)

    fr = np.repeat(fr[::2],2)

    channel_left = fr[::2]
    channel_right = fr[1::2]
    wave_val, channel_left_transformed = transform_left_channel(obj, channel_left, transformation=np.sin)
    channel_right_transformed = transform_right_channel(obj, channel_right, transformation=np.sin)

    channel_left[:] = channel_left_transformed
    channel_right[:] = channel_right_transformed

    return fr

def transform_left_channel(obj, channel, transformation= np.sin):
    rot_speed = 2
    step = np.pi/(len(channel)/rot_speed)
    wave_val = np.arange(0,np.pi, step)
    wave_val = np.tile(wave_val, rot_speed)
    wave_val = transformation(wave_val)
    for i,val in enumerate(wave_val):
        wave_val[i] = pow(2, (np.sqrt(np.sqrt(np.sqrt(val))) * 192 - 192)/6)
    tmp = channel.copy()
    for i, val in enumerate(tmp):
        tmp[i] = val*wave_val[i]
    return wave_val, tmp

def transform_right_channel(obj, channel, transformation= np.sin):
    rot_speed = 2
    step = np.pi/(len(channel)/rot_speed)
    wave_val = np.arange(0,np.pi, step)
    wave_val = np.tile(wave_val, rot_speed)
    wave_val = transformation(wave_val)
    for i,val in enumerate(wave_val):
        wave_val[i] = pow(2, (np.sqrt(np.sqrt(np.sqrt(1-val))) * 192 - 192)/6)
    tmp = channel.copy()
    for i, val in enumerate(tmp):
        tmp[i] = val*wave_val[i]
    return tmp

def run():
    global nchannels
    input = "speech.wav"
    output = "output2.wav"


    obj = wave.open(input, "rb")
    print(obj.getparams())
    nchannels = obj.getnchannels()

    frames = obj.readframes(-1)
    fr = np.frombuffer(frames, dtype=np.int16)
    fr = fr.copy()
        
    #fr = addEcho(obj, fr, 0.2, 0.7)
    #fr = muffleFft(obj,fr)
    fr = audio360(obj, fr)

    obj_new = wave.open(output, "wb")
    obj_new.setnchannels(nchannels)
    obj_new.setsampwidth(obj.getsampwidth())
    obj_new.setframerate(obj.getframerate())
    obj_new.writeframes(b''.join(fr))
    return Audio(filename=output)
