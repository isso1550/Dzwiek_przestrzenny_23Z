import filemanager
import panning
import delay
import distance
import hrir
from numpy import pi, rad2deg

input = "../Audio/speech.wav"
input = "../Audio/NewJeans-_뉴진스_-ETA-Official-MV-_Performance-ver._.wav"
#input = "..\Audio\Michael Jackson - Beat It (Official Audio).wav"
output = "../Audio/mainoutput.wav"

distance_from_source = 4
angle_offset = 0
hrir_angle = 45
Pan_using_HRIR = True

center_angle = pi/2
angle = center_angle + angle_offset



#distance.DistanceByGain(input, output, 20)
#distance.ProgressiveDistanceByGain(input, output, 1, 20)
if (distance_from_source > 1):
    print(f"Przetwarzanie sygnalu: symulacja odleglosci d = {distance_from_source} metrów")
    distance.DistanceByGainHighshelf(input, output, 4)
    input = output


fr, obj = filemanager.loadSignal(input)
fs = obj.getframerate()
left, right = filemanager.getStereoChannels(fr, obj)

if Pan_using_HRIR:
    hrir.HRIRPan(input, output, hrir_angle)

elif (angle != center_angle):
    print(f"Przetwarzanie sygnalu: symulacja kąta alfa = {rad2deg(angle_offset)} stopni od godziny 12 idąc zgodnie ze wskazówkami")
    if(angle > pi):
        angle = angle - pi
    left, right = panning.ConstantPowerPan(angle, left, right)
    left, right = delay.delay(angle, left, right, fs)
    filemanager.saveStereoSignal(obj, left, right, output)





