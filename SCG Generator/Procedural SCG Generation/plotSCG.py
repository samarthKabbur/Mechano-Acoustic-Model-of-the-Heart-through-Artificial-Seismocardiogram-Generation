from matplotlib import pyplot as plt
import pandas as pd
import scipy.signal as signal
import numpy as np
import os

#Constants
freq = 256 # in hz
column_names = [
    'ticks',
    'scgx',
    'scgy',
    'scgz'
    #load only columns 1-4
    #the rest are ECG related
]

# Reading File
data = pd.read_csv("CP-01-Raw.csv")
time = data.

