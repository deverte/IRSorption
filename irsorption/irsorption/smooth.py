import pandas as pd
from scipy import signal

def smooth(data, N, Wn):
    b, a = signal.butter(N, Wn, 'low')
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, data, zi=zi*data[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
    smoothed = pd.DataFrame(data=signal.filtfilt(b, a, data), index=data.index)
    return smoothed