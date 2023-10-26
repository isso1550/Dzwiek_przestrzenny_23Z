import filemanager
from numpy import max, arctan, rad2deg, where, abs, arcsin, pi, deg2rad

def guessAngle(filename):
    fr, obj = filemanager.loadSignal(filename)
    left, right = filemanager.getStereoChannels(fr, obj)
    print("Kąty podane są idąc od godziny 12 na tarczy zegara zgodnie z ruchem wskazówek")
    try:
        #Badanie na podstawie maksymalnych amplitud
        #Dziala duzo lepiej dla CPP
        l = max(left)
        r = max(right)
        angle = arctan(r/l)*2
        angle = 90-rad2deg(angle)
        if (l>r):
            angle = angle * -1
        print(f"Przypuszczenie na podstawie roznic w amplitudach przy zalozeniu CPP: {angle}")
    except Exception as e:
        print(f"Niestety cos poszlo nie tak przy analizie roznic w amplitudach")
    try:
        #Badanie na podstawie maksymalnych amplitud
        #Dziala duzo lepiej dla LP
        angle = pi/(l/r + 1)
        angle = rad2deg(angle)
        angle = 90 - angle
        if (l>r):
            angle = angle * -1
        print(f"Przypuszczenie na podstawie roznic w amplitudach przy zalozeniu LP: {angle}")
    except Exception as e:
        print(f"Niestety cos poszlo nie tak przy analizie roznic w amplitudach")
    try:
        #Badanie na podstawie przesuniecia
        #Przy innych parametrach predkosci dzwieku i szerokosci glowy przypuszczenie bedzie dalsze od prawdy, ale powinno wciaz pozwolic
        #na osobista ocene
        lid = where(left == l)[0]
        rid = where(right == r)[0]
        ndelay = abs(rid-lid) #wykryc strone!
        speed_of_sound = 345
        headwidth = 0.15
        sa = ndelay/obj.getframerate()*speed_of_sound/headwidth
        angle = rad2deg(arcsin(sa))
        if rid > lid:
            angle = angle * -1
        print(f"Przypuszczenie na podstawie przesuniecia syngalow: {angle}")
    except Exception as e:
        print(f"Niestety cos poszlo nie tak przy analizie przesuniecia sygnalow, probuje drugiej metody!")

    try:
        #Alternatywna metoda - program wycina kawalek ze srodka sygnalu i ponawia probe
        #Jesli srodek sygnalu to cisza to niestety nie uda sie zgadnac
        w1 = left[round(len(left)/2):round(len(left)/2 + 1000)]
        w2 = right[round(len(left)/2):round(len(left)/2 + 1000)]
        l = max(w1)
        r = max(w2)
        lid = where(w1 == l)[0]
        rid = where(w2 == r)[0]
        ndelay = abs(rid-lid) #wykryc strone!
        speed_of_sound = 345
        headwidth = 0.15
        sa = ndelay/obj.getframerate()*speed_of_sound/headwidth
        angle = rad2deg(arcsin(sa))
        if rid > lid:
            angle = angle * -1
        print(f"Przypuszczenie na podstawie analizy przesuniecia sygnalow alternatywna metoda: {angle}")
    except Exception as e:
        print(f"Niestety cos poszlo nie tak przy analizie przesuniecia sygnalow druga metoda")