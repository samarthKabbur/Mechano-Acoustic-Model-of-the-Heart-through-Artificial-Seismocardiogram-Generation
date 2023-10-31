import numpy as np
from scipy import signal

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_filter(btype, data, cutoff, fs, order=5):
    
    if btype == 'high': 
        b, a = butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y
    elif btype == 'low': 
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y
    
def mchan_ceil(arr, decimal=0): 
    return np.ceil(arr*(10**-decimal))/(10**-decimal)

def mchan_floor(arr, decimal=0):
    return np.floor(arr*(10**-decimal))/(10**-decimal)