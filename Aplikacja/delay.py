from numpy import pi, sin, int16
from numpy import concatenate, zeros, round

def delay(angle, leftSignal, rightSignal, framerate, headwidth=0.15, speed_of_sound=345):
    #Kat wejsciowy z przedzialu 0 180
    if (angle > pi/2):
        #Opoznij lewy kanal
        toDelay = leftSignal.copy()
        toCopy = rightSignal.copy()
    elif (angle < pi/2):
        #Opoznij prawy kanal
        toDelay = rightSignal.copy()
        toCopy = leftSignal.copy()
    else:
        return leftSignal, rightSignal
    #Wspolczynnik -> max dla katow 0 i 180, wartosc srodkowa dla 90
    a = sin(angle + pi/2)
    #Liczba klatek opoznienia = czas na pokonanie odcinka * framerate
    ndelay = (a*headwidth/speed_of_sound) * framerate
    #nframes = len(toDelay)
    ndelay = int(abs(round(ndelay)))
    #print(f"ldel = {ldel},  a = {a} , ndelay = {ndelay}")

    delayedSig = concatenate((zeros(ndelay), toDelay[:-ndelay])).astype(int16)
    
    if (angle > pi/2):
        return delayedSig, toCopy
    else:
        return toCopy, delayedSig

