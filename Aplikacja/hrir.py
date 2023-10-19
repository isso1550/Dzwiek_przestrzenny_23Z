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
    fr = lr.resample(fr, orig_sr=frsr, target_sr=irsr)
    s_R = convolve(fr,irfr[:,0])
    s_L = convolve(fr,irfr[:,1])
    mix = vstack([s_R, s_L])
    sf.write(output, mix.transpose(), irsr)