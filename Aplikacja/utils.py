from scipy.signal import butter, sosfilt
from numpy import round, int16

def muffle(sig, fs, Wn):
    #Experimental
    if len(sig) == 0:
        return sig
    #Wn 10k?
    sos = butter(10, Wn, 'lp', fs=fs, output='sos')
    filtered = sosfilt(sos, sig)
    filtered = round(filtered).astype(int16)
    return filtered