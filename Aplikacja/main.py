import filemanager
import panning
import delay
from numpy import pi

input = "../Audio/speech.wav"
input = "../Audio/NewJeans-_뉴진스_-ETA-Official-MV-_Performance-ver._.wav"
output = "../Audio/mainoutput.wav"

fr, obj = filemanager.loadSignal(input)
fs = obj.getframerate()
left, right = filemanager.getStereoChannels(fr, obj)

#angle = pi/2 + pi/4
#left, right = panning.ConstantPowerPan(angle, left, right)
#left, right = delay.delay(angle, left, right, fs)

left, right = panning.Pan8d(left, right, fs, 5, 8)

filemanager.saveStereoSignal(obj, left, right, output)