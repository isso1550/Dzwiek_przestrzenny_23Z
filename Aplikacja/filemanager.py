import wave
from numpy import frombuffer, int16, insert, arange

def loadSignal(filename):
    #Zwraca wektor klatek oraz obiekt wave na podstawie sciezki do pliku
    obj = wave.open(filename, "rb")
    fr = frombuffer(obj.readframes(-1), dtype=int16)
    return fr, obj

def getStereoChannels(fr, obj):
    nchannels = obj.getnchannels()
    if nchannels > 1:
        left = fr[1::2]
        right = fr[::2]
    else:
        left = right = fr
    return left, right


def saveStereoSignal(obj, left, right, filename):
    #Zapisuje dzwiek dwukanalowy (left, right) na podstawie obiektu wave, wektorow amplitud oraz 
    #sciezki pliku wyjsciowego
    framerate = obj.getframerate()
    sampwidth=obj.getsampwidth()
    signal = insert(right, arange(len(left)), left)
    nchannels = 2
    obj_new = wave.open(filename, "wb")
    obj_new.setnchannels(nchannels)
    obj_new.setsampwidth(sampwidth)
    obj_new.setframerate(framerate)
    obj_new.writeframes(signal)
    return True

