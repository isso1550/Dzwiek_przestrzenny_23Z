from numpy import pi, sin, cos, int16
from numpy import arange, concatenate, flip, ceil , tile, negative, int16

def Pan(leftSignal, rightSignal, amp_L, amp_R, returnAmplitudes):
    if(returnAmplitudes):
        return amp_L, amp_R
    else:
        leftSignal = (leftSignal * amp_L).astype(int16)
        rightSignal = (rightSignal * amp_R).astype(int16)
        #print(amp_L, amp_R)
        return leftSignal, rightSignal
    
def LinearPan(angle, leftSignal, rightSignal, returnAmplitudes = False):
    #print("Linear panning")
    amp_L = 1 - angle/pi
    amp_R = angle/pi

    return Pan(leftSignal, rightSignal, amp_L, amp_R, returnAmplitudes)

def ConstantPowerPan(angle, leftSignal, rightSignal, returnAmplitudes = False, progiMin = False, progiMax = False):
    #print("Constant power panning")
    amp_L = cos(angle/2)
    amp_R = sin(angle/2) 

    #TO na pozniej - bardziej realny efekt
    if progiMin:
        if (amp_R) < 0.15:
            amp_R = 0.15
        if (amp_L) < 0.15:
            amp_L = 0.15
    if progiMax:
        if (amp_R) > 0.92:
            amp_R = 0.92
        if (amp_L) > 0.92:
            amp_L = 0.92
    return Pan(leftSignal, rightSignal, amp_L, amp_R, returnAmplitudes)



def Pan8d(leftSignal, rightSignal, framerate, step, rot_seconds, method=ConstantPowerPan, progiMin=False, progiMax=False):
    #Utworzenie plynnego przejscia od 0 do 180 stopni z krokiem step
    angles = arange(0, pi, pi*step/180)
    #Polączenie przejscia 0-180 z odwrotnoscia (180-0), aby uzyskac przejscie 0-360
    angles = concatenate( (angles, negative(flip(angles)) ))

    #Okno, czyli ile klatek bedzie pochodzilo z tego samego kierunku
    #Okno = int ( Czas trwania obrotu [s] * Czestotliwosc probkowania / Liczbe kierunkow )
    window = int(rot_seconds * framerate / len(angles))

    #Ile powtorzeń wymaga wektor kątów, aby pokryć caly sygnal
    nframes = len(leftSignal)

    #Powtorzenia = zaokrąglony w górę int ( liczba klatek / czestotliwosc probkowania / czas trwania obrotu [s])
    repeats = int(ceil(nframes/framerate/rot_seconds))
    angles = tile(angles, repeats)

    left = leftSignal.copy()
    right = rightSignal.copy()

    left2 = left * 0
    right2 = right * 0
    #left2 = zeros(len(leftSignal)+30, dtype = type(leftSignal[0]))
    #right2 = zeros(len(rightSignal)+30, dtype = type(rightSignal[0]))

    #Glowna petla
    #Przesun okno -> przeksztalc wycinek dla odpowiadajacego kata -> dolacz do lacznego sygnalu
    if (method == ConstantPowerPan):
        for i in range(0, len(angles)):
            angle = abs(angles[i])     
            new_L, new_R = method(angle, left[i*window:(i+1)*window], right[i*window:(i+1)*window], progiMin=progiMin, progiMax=progiMax)
            left2[i*window:(i+1)*window], right2[i*window:(i+1)*window] = new_L, new_R

        left = left2
        right = right2     
    else:
        for i in range(0, len(angles)):
            angle = abs(angles[i])      
            new_L, new_R = method(angle, left[i*window:(i+1)*window], right[i*window:(i+1)*window])
            left[i*window:(i+1)*window], right[i*window:(i+1)*window] = new_L, new_R
    return left, right


#https://medium.com/klinke-audio/a-detailed-overview-of-panning-functions-dc58f6d94b94