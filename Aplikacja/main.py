import filemanager
import panning
import delay
import distance
import hrir
import argparse
from numpy import pi, rad2deg, deg2rad

input = "../Audio/speech.wav"
input = "../Audio/NewJeans-_뉴진스_-ETA-Official-MV-_Performance-ver._.wav"
#input = "..\Audio\Michael Jackson - Beat It (Official Audio).wav"
output = "../Audio/mainoutput.wav"

parser = argparse.ArgumentParser(description='Dzwiek przestrzenny')
parser.add_argument('input', metavar='input_path', type=str, nargs="?", default=input,
                    help='Sciezka do pliku wejsciowego')
parser.add_argument('output', metavar='output_path', type=str, nargs="?", default=output,
                    help='Sciezka, gdzie ma zostac zapisany wynik')
parser.add_argument('-auto', '--auto', action="store_true",
                    help='Automatycznie ustaw parametry dzwieku przestrzennego')
parser.add_argument('-a', '--angle', type=int, nargs="?", default=45, choices=range(-90,90+1,5), metavar="-90 - +90, krok 5",
                    help='Kąt kierunku od sluchacza do zrodla. Liczony jako zakres -90 do 90 od godziny 9 do 3 zgodnie z ruchem wskazowek.')
parser.add_argument('-p', '--pan', choices=['cpp','lp'],
                    help='Wykonaj panning cpp lub lp')
parser.add_argument('-d', '--delay', action="store_true",
                    help='Dodaj opoznienie kanalu')
parser.add_argument('-hrir', '--hrir', action="store_true",
                    help='Wykonaj panning przez splot HRIR')
parser.add_argument('-c8d', '--create8d', action="store_true",
                    help='Wykonaj panning 8D')
parser.add_argument('-rd', '--rotdur', type=int, nargs="?", default=15,
                    help='Czas trwania obrotu w dzwieku 8d')
parser.add_argument('-ds', '--distance', type=int, nargs="?", default=1,
                    help='Odleglosc zrodla od sluchacza [m]')


args = parser.parse_args()

input = args.input
output = args.output

distance_from_source = args.distance
if (args.auto):
    pan_method = "cpp"
    delaySig = True
else:
    pan_method = args.pan
    delaySig = args.delay
angle_offset = args.angle

Pan_using_HRIR = args.hrir
hrir_angle = args.angle

create8d = args.create8d
rotation_duration_8d = args.rotdur

center_angle = pi/2
angle = center_angle + deg2rad(angle_offset)
#ngle = angle_offset

if(create8d):
    print(f"Przetwarzanie pliku {input}. Parametry:\n-Audio 8D = {create8d}\n-Czas trwania obrotu = {rotation_duration_8d}\nZapis do pliku {output}")
elif(Pan_using_HRIR):
    print(f"Przetwarzanie pliku {input}. Parametry:\n-Kąt = {angle_offset}\n-HRIR = {Pan_using_HRIR}\nZapis do pliku {output}")
else:
    print(f"Przetwarzanie pliku {input}. Parametry:\n-Kąt = {angle_offset}\n-Metoda panningu = {pan_method}\n-Opoznienie = {delaySig}\nZapis do pliku {output}")

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

if pan_method != None:
    if (angle != center_angle):
        print(f"Przetwarzanie sygnalu: symulacja kąta alfa = {angle_offset} stopni od godziny 12 idąc zgodnie ze wskazówkami")
        if(angle > pi):
            angle = angle - pi
        if(pan_method == "cpp"):
            left, right = panning.ConstantPowerPan(angle, left, right, progiMin=True, progiMax=True)
        else:
            left,  right = panning.LinearPan(angle, left, right)

        if(delaySig):
            left, right = delay.delay(angle, left, right, fs)
        filemanager.saveStereoSignal(obj, left, right, output)
    else:
        print("Podany kąt odpowiada prostemu kierunkowi, podaj inny kąt!")
        exit()

if create8d:
    left,right = panning.Pan8d(left, right, obj.getframerate(), 5, rotation_duration_8d, panning.ConstantPowerPan, progiMin=True,progiMax=True)
    filemanager.saveStereoSignal(obj, left, right, output)





