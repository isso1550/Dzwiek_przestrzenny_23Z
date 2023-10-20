from numpy import convolve, vstack
import librosa as lr
import soundfile as sf

def HRIRPan(input, output, degrees, library_path = "../HRIR/diffuse/elev0/"):
    fr, frsr = sf.read(input)
    if degrees > 99:
        input = library_path + "H0e" + str(degrees) + "a.wav"
    else:
        input = library_path + "H0e0" + str(degrees) + "a.wav"
    irfr, irsr = sf.read(input)
    print(input)
    if (frsr < irsr):
        print("Resampling input...")
        fr = lr.resample(fr, orig_sr=frsr, target_sr=irsr)
    elif (frsr > irsr):
        print("Resampling impulse response...")
        irfr = lr.resample(irfr, orig_sr=irsr, target_sr=frsr)
        irsr = frsr

    if (len(fr.shape) > 1 and fr.shape[1] >= 2):
        print(len(fr[:,0]))
        s_R = convolve(fr[:,0],irfr[:,0])
        s_L = convolve(fr[:,1],irfr[:,1])
    else:
        print("2")
        s_R = convolve(fr,irfr[:,0])
        s_L = convolve(fr,irfr[:,1])
    print("saving")
    mix = vstack([s_R, s_L])
    sf.write(output, mix.transpose(), irsr)