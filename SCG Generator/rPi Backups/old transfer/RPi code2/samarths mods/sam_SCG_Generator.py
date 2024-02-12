import RPi.GPIO as GPIO
from time import sleep
from time import time
import threading
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

import multiprocessing as mp
import random

import sys
from pygame import mixer
import subprocess
import os
import os.path
from scipy.fftpack import fft, fftfreq, fftshift, rfft, ifft
from scipy import signal

import wave
import struct
import ctypes
import scipy.io.wavfile
import scipy
# import plotext as plx

import csv

import pickle

# from threading import Thread, current_thread

from sam_adxl355 import ADXL355
import customfilter

import smbus
import time
bus = smbus.SMBus(1)
address = 0x48


## calibrate each beat using the transfer function
## how the filter will modify the frequency content of a signal, and to design the filter to achieve a desired frequency response.
def calibrate_beat(beat,beat_sample_rate,transfer_funtion,transfer_funtion_freq,plot=False):

    beat_fft = (fft(beat,beat.shape[-1]))
    beat_fft_freq = (fftfreq(beat.shape[-1],d=1/(beat_sample_rate)))

    controller = np.ones(len(beat_fft))

    for i in range(len(beat_fft_freq)):

        idx = np.argmin(np.abs(transfer_funtion_freq - np.abs(beat_fft_freq[i])))

        if (transfer_funtion[idx]!=0) and beat_fft_freq[i]<40:
            controller[i] = 1/transfer_funtion[idx]
       
        else: 
            controller[i] = 0
            

    calibrated = np.multiply(beat_fft, controller)

    # calibrated = calibrated.real
    calibrated = ifft(calibrated)
    
    #if plot:
        #plt.figure()
        #plt.plot(calibrated)
       # plt.show()  

    
    return calibrated, beat_sample_rate

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    
        
GPIO.setmode(GPIO.BOARD)

   
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


## function for saving the audio files ready for generation
def save_wav(file_name,SCG_audio,ECG_audio,sample_rate=500):
    
    # Open up a wav file
    wav_file=wave.open(file_name+"_SCG.wav","w")

    # wav params
    nchannels = 2
    
    #number of bytes per sample
    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(SCG_audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    
#     SCG_audio=SCG_audio/np.max(abs(SCG_audio))
#     SCG_audio=SCG_audio/3
    
    for s, t in zip(SCG_audio,-SCG_audio):
        wav_file.writeframes(struct.pack('h', int( s * 32767.0 )))
        wav_file.writeframes(struct.pack('h', int( t * 32767.0 )))

    wav_file.close()
    
    wav_file2=wave.open(file_name+"_ECG.wav","w")
    nframes = len(ECG_audio)
    wav_file2.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))


#     ECG_audio=ECG_audio/np.max(abs(ECG_audio))
#     ECG_audio=ECG_audio/3
    
    for s, t in zip(ECG_audio,-ECG_audio):
        wav_file2.writeframes(struct.pack('h', int( s * 32767.0 )))
        wav_file2.writeframes(struct.pack('h', int( t * 32767.0 )))

    wav_file2.close()
    
    return
    
    
    
## function for reading acceleration using the onboard ADXL355
def adxl_process(z_axis,startRec,doneRec):

    accel.read_FIFO(84*3)
    while True:
        
        if doneRec.value:
            print("stopping reading")
            return
        
        while (accel.FIFO_cnt()<84):
            continue

        if accel.FIFO_cnt()>92:
            print(bcolors.WARNING + "warning: Overflow"+ bcolors.RESET)
            
        fifoData = accel.read_FIFO(84*3)
        
        if startRec.value:
            for i in range(0,84*3,9):
                z_axis.append( twos_comp((fifoData[i+6]<<12)|(fifoData[i+7]<<4)|(fifoData[i+8]>>4) , 20) )


# def calibrate_process(z_axis,startRec,doneRec,cal_data,fileName):

#     startRec.value=0
#     doneRec.value=1
    

# #     with  open("transfer_function/transfer_function.pkl",'rb') as file:
#     with  open("transfer_function/transfer_function_RPi.pkl",'rb') as file:

#         object_file = pickle.load(file)
#     # print(object_file.keys())
#     transfer_funtion = object_file.get('transfer_function')
#     transfer_funtion_freq = object_file.get('transfer_function_freq')

#     dataset_dir = 'real_beats/sequences/'+fileName[0]+'.pkl'

#     plt.figure()
#     plt.plot(transfer_funtion_freq, transfer_funtion)
#     plt.show()
    
#     with  open(dataset_dir,'rb') as file:
#         object_file = pickle.load(file)

#     print(object_file.keys())
#     scg_reduce = 1
#     ecg_reduce = 10
#     scg_beats = object_file.get('scg_beats')/scg_reduce
#     R_peaks = object_file.get('R_peaks').astype(int)
# #     print(R_peaks*4)
#     ecg_beats = object_file.get('ecg_beats')/ecg_reduce
    
#     SCG_sequence = object_file.get('scg_seq')/scg_reduce
#     ECG_sequence = object_file.get('ecg_seq')/ecg_reduce
    
#     beat_sample_rate_old = 250 #1000
#     beat_sample_rate = 1000
    
#     ## to initialize the sequence with real sequence
# #     beat_len_upsampled = int(len(SCG_sequence)*(beat_sample_rate/beat_sample_rate_old))
# #     SCG_sequence = signal.resample(SCG_sequence, beat_len_upsampled)
    
# #     beat_len_upsampled = int(len(ECG_sequence)*(beat_sample_rate/beat_sample_rate_old))
# #     ECG_sequence = signal.resample(ECG_sequence, beat_len_upsampled)
# #     # print(type(ECG_sequence[0]))
    
#     ## to initialize the sequence with zeros
#     beat_len_upsampled = int(len(SCG_sequence)*(beat_sample_rate/beat_sample_rate_old))
#     SCG_sequence = np.zeros(int(beat_len_upsampled))
#     # SCG_sequence = np.zeros(int(R_peaks[-1]*4+1000))
#     beat_len_upsampled = int(len(ECG_sequence)*(beat_sample_rate/beat_sample_rate_old))
#     ECG_sequence = np.zeros(int(beat_len_upsampled))
#     # ECG_sequence = np.zeros(int(R_peaks[-1]*4+1000))
    
#     beat_len = 125 #len(scg_beats[:,i])
#     beat_sample_rate_old = 250 #1000


#     poor_beats = 0
#     poor_beats_idx = []
#     beat_sample_rate = 1000
#     R_peaks = R_peaks*(beat_sample_rate/beat_sample_rate_old)
#     print('SCG Irg range: {}'.format([np.max(SCG_sequence), np.min(SCG_sequence)]))
#     print('ECG Org range: {}'.format([np.max(ECG_sequence), np.min(ECG_sequence)]))
#     for i, _ in enumerate(R_peaks):

#         if (i % 1000) == 0:
#             print(str(i) + ' of ' + str(R_peaks.shape[0]))
#         beat_len_upsampled = int(beat_len*(beat_sample_rate/beat_sample_rate_old))
# #         print(f"beat len = {beat_len_upsampled}")
#         #beat = scg_beats[:,i][:125].copy()
#         #beat = signal.resample(beat, beat_len_upsampled)

#         # if we are not at the end 
#         if i < R_peaks.shape[0] - 1:
            
#             # if we are between two subject 
#             # assumed 1000Hz so if the difference in r peaks is greater than 4 seconds
#             if R_peaks[i+1] - R_peaks[i] > 4000:
#                 beat = SCG_sequence[int(R_peaks[i])-80:int(R_peaks[i])-80+3000]
#                 idx_start = int(R_peaks[i])-80
#                 idx_end = int(R_peaks[i])-80+3000
#             else:

#                 beat = SCG_sequence[int(R_peaks[i])-80:int(R_peaks[i+1])-80]
#                 idx_start = int(R_peaks[i])-80
#                 idx_end = int(R_peaks[i+1])-80
#         else:
#             beat = SCG_sequence[int(R_peaks[i])-80:int(R_peaks[i])-80+3000]
#             idx_start = int(R_peaks[i])-80
#             idx_end = int(R_peaks[i])-80+3000

#         ecg_beat = ecg_beats[:,i][:125].copy()
#         ecg_beat = signal.resample(ecg_beat, beat_len_upsampled)

#         y, _ = calibrate_beat(beat,beat_sample_rate,transfer_funtion,transfer_funtion_freq,plot=False)

#         #y=y/10  #synth
#         y=y/(120)
#         ecg_beat=ecg_beat/8   ## to increase ECG amplitude
#         y=-y
#         if (max(y) > 1.0) | (min(y) < -1.0):
#             poor_beats += 1
#             poor_beats_idx.append(i)
# #         print(R_peaks[i])
#         #SCG_sequence[int(R_peaks[i])-80: beat_len_upsampled + int(R_peaks[i])-80] = y.copy()
#         SCG_sequence[idx_start:idx_end] = y.copy()

# #         r_loc = (np.argmax(ecg_beat))
#         r_loc = 80
#         ECG_sequence[int(R_peaks[i])-r_loc: beat_len_upsampled + int(R_peaks[i])-r_loc] = ecg_beat.copy()

            
#     SCG_audio=SCG_sequence
#     ECG_audio=ECG_sequence

#     lowcutoff = 0.6
#     highcutoff = 40
#     ECG_audio = customfilter.butter_filter('high',ECG_audio,lowcutoff,beat_sample_rate)
#     ECG_audio = customfilter.butter_filter('low',ECG_audio,highcutoff,beat_sample_rate)
# #     ECG_audio = ECG_audio - ECG_audio[-1]
    
#     lowcutoff = 1
#     highcutoff = 50#30
#     SCG_audio = customfilter.butter_filter('high',SCG_audio,lowcutoff,beat_sample_rate)
#     SCG_audio = customfilter.butter_filter('low',SCG_audio,highcutoff,beat_sample_rate)
# #     SCG_audio = SCG_audio - SCG_audio[-1]
#     SCG_audio[np.where((SCG_audio < -1.0))] = -1.0
#     SCG_audio[np.where((SCG_audio > 1.0))] = 1.0
#     print('SCG Audio range: {}'.format([np.max(SCG_audio), np.min(SCG_audio)]))
#     print('ECG Audio range: {}'.format([np.max(ECG_audio), np.min(ECG_audio)]))
# #
#     print('Poor Beat Idx: {}',format(poor_beats_idx))
#     print(str(poor_beats) + ' of ' + str(R_peaks.shape[0]) + ' beats exceed range')
#     if(fileName[1]=="desktop"):
#                 plt.figure()
#                 plt.plot(np.arange(0,len(ECG_audio))*1/1000,ECG_audio,color='r')
#                 plt.plot(np.arange(0,len(SCG_audio))*1/1000,SCG_audio,color='b')
#                 plt.title("SCG sequence")
#                 plt.show()
#     else:
#                 plx.clp()
#                 plx.plot(np.arange(0,len(ECG_audio))*1/1000,ECG_audio,color='r')
#                 plx.plot(np.arange(0,len(SCG_audio))*1/1000,SCG_audio,color='b')
#                 plx.plotsize(100,30)
#                 plx.title("SCG sequence")
#                 plx.show()  

#     cal_data.append(ECG_audio.copy())
#     cal_data.append(SCG_audio.copy())
    
#     return

## function for calibrating the beats using the estimated transfer function
def calibrate_process(z_axis,startRec,doneRec,cal_data,fileName):


    startRec.value=0
    doneRec.value=1
    

#     with  open("transfer_function/transfer_function.pkl",'rb') as file:
    with  open("transfer_function/transfer_function_RPi.pkl",'rb') as file:

        object_file = pickle.load(file)
    # print(object_file.keys())
    transfer_funtion = object_file.get('transfer_function')
    transfer_funtion_freq = object_file.get('transfer_function_freq')

    dataset_dir = 'real_beats/sequences/'+fileName[0]+'.pkl'

   # plt.figure()
   # plt.plot(transfer_funtion_freq, transfer_funtion)
  #  plt.show()
    
    with  open(dataset_dir,'rb') as file:
        object_file = pickle.load(file)

    print(object_file.keys())
    scg_reduce = 1
    ecg_reduce = 10
    scg_beats = object_file.get('scg_beats')/scg_reduce
    R_peaks = object_file.get('R_peaks').astype(int)

    ecg_beats = object_file.get('ecg_beats')/ecg_reduce
    
    SCG_sequence = object_file.get('scg_seq')/scg_reduce
    ECG_sequence = object_file.get('ecg_seq')/ecg_reduce
    
    beat_sample_rate_old = 250 #1000
    beat_sample_rate = 1000
    
    beat_len_upsampled = int(len(SCG_sequence)*(beat_sample_rate/beat_sample_rate_old))
    SCG_sequence = signal.resample(SCG_sequence, beat_len_upsampled)
    
    beat_len_upsampled = int(len(ECG_sequence)*(beat_sample_rate/beat_sample_rate_old))
    ECG_sequence = signal.resample(ECG_sequence, beat_len_upsampled)
    # print(type(ECG_sequence[0]))

    SCG_sequence = np.zeros(int(R_peaks[-1]*4+1000))
    ECG_sequence = np.zeros(int(R_peaks[-1]*4+1000))
    
    for i, _ in enumerate(R_peaks):
        beat_len = 125 #len(scg_beats[:,i])
        beat_sample_rate_old = 250 #1000

        beat_sample_rate = 1000
        R_peaks[i] = R_peaks[i]*(beat_sample_rate/beat_sample_rate_old)
        beat_len_upsampled = int(beat_len*(beat_sample_rate/beat_sample_rate_old))

        beat = scg_beats[:,i][:125].copy()
        beat = signal.resample(beat, beat_len_upsampled)
        
        ecg_beat = ecg_beats[:,i][:125].copy()
        ecg_beat = signal.resample(ecg_beat, beat_len_upsampled)
        
        y, _ = calibrate_beat(beat,beat_sample_rate,transfer_funtion,transfer_funtion_freq,plot=False)
        y = y-y[480]
        y[480:]=0

        y=y/(120)
        ecg_beat=ecg_beat/8   ## to increase ECG amplitude
        y=-y
    
        SCG_sequence[int(R_peaks[i])-80: beat_len_upsampled + int(R_peaks[i])-80] = y.copy()
        r_loc = 80
        ECG_sequence[int(R_peaks[i])-r_loc: beat_len_upsampled + int(R_peaks[i])-r_loc] = ecg_beat.copy()

            
    SCG_audio=SCG_sequence
    ECG_audio=ECG_sequence

    lowcutoff = 0.6
    highcutoff = 40
    ECG_audio = customfilter.butter_filter('high',ECG_audio,lowcutoff,beat_sample_rate)
    ECG_audio = customfilter.butter_filter('low',ECG_audio,highcutoff,beat_sample_rate)
    
    lowcutoff = 1
    highcutoff = 50#30
    SCG_audio = customfilter.butter_filter('high',SCG_audio,lowcutoff,beat_sample_rate)
    SCG_audio = customfilter.butter_filter('low',SCG_audio,highcutoff,beat_sample_rate)
#     SCG_audio = SCG_audio - SCG_audio[-1]
#     print('SCG Audio range: {}'.format([np.max(SCG_audio), np.min(SCG_audio)]))
#     print('ECG Audio range: {}'.format([np.max(ECG_audio), np.min(ECG_audio)]))
    
    if(fileName[1]=="desktop"):
               # plt.figure()
              # plt.plot(np.arange(0,len(ECG_audio))*1/1000,ECG_audio,color='r')
               # plt.plot(np.arange(0,len(SCG_audio))*1/1000,SCG_audio,color='b')
               # plt.title("SCG sequence")
               # plt.show()
               print("hello")
    else:
            plx.clp()
            plx.plot(np.arange(0,len(ECG_audio))*1/1000,ECG_audio,color='r')
            plx.plot(np.arange(0,len(SCG_audio))*1/1000,SCG_audio,color='b')
            plx.plotsize(100,30)
            plx.title("SCG sequence")
            plx.show()  

    cal_data.append(ECG_audio.copy())
    cal_data.append(SCG_audio.copy())
    
    return

## function for transfer function estimation
def tf_estimate_process(z_axis,startRec,doneRec,cal_data,fileName):

    sleep(2)
    startRec.value=1
    print(bcolors.OK + 'starting sweep' + bcolors.RESET)

#     sound = mixer.Sound('sweep_fg_1.wav')
    
#     os.system('omxplayer -o local sweep_fg_1.wav')
#    
    
    
## making sure channel 0 is producing the sweep
    mixer.pre_init(100000,-16,2)
    mixer.init()
    print(f"Initialized: {mixer.get_init()}")
    mixer.set_num_channels(2)
    print(f"Number of channels: {mixer.get_num_channels()}")
    
    sound0=mixer.Sound("sweep_fg_1.wav")
    channel0=mixer.Channel(0)
    channel0.set_volume(0.0,0.2)
    
    channel1=mixer.Channel(1)
    channel1.set_volume(0.0 ,0.0)  ## to increase ECG amplitude
    
    channel0.play(sound0)
#     channel1.play(sound1)

    while channel0.get_busy() == True:
        continue
    
    while channel1.get_busy() == True:
        continue
    
## old code    
#     mixer.pre_init(100000,-16,2)
#     mixer.init()
#     mixer.music.load("sweep_fg_1.wav")
#     mixer.music.set_volume(0.2)
#     mixer.music.play()
#     while mixer.music.get_busy() == True:
#         continue
    
    print(bcolors.OK +'done sweep'+ bcolors.RESET)
    
    startRec.value=0
    doneRec.value=1
    
    sleep(2)
    
    data=list(z_axis).copy()
    
    data=[float(i)*0.0078*-1 for i in data]
    data=np.asarray(data)
    data=data-np.mean(data)

    print("Plotting...")
    if(fileName[0]=="desktop"):
       # plt.figure()
        #plt.plot(range(len(data)),data)
        #plt.title("Output of Sweep")
       # plt.show()
       print('hello')
    else:
        plx.clp()
        plx.plot(range(len(data)),data)
        plx.plotsize(100,30)
        plx.title("Output of Sweep")
        plx.show()
    print("Calculating FFT")
    
    SAMPLE_RATE=1000
    N = len(data)
# 
    yf = fft(data)
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    yf= fftshift(yf)
    xf= fftshift(xf)

    
    NFFT=len(xf)
    freqs, psd = signal.welch(data,SAMPLE_RATE,window='hamm', noverlap=10,detrend='constant', nfft=NFFT, return_onesided=True, scaling='spectrum')
#     freqs, psd = signal.periodogram(data,SAMPLE_RATE, window='hann', nfft=NFFT,scaling='spectrum')
    psd=psd**0.5
    
    print(freqs)
#     plt.figure()
    print("Plotting PSD...")
    if(fileName[0]=="desktop"):
        #plt.figure()
       # plt.plot(freqs, 10*np.log10(psd) )
        #plt.title("PSD of Sweep Output")
       # plt.show()
       print('ehhlo')
    else:
        plx.clp()
        plx.plot(freqs, 10*np.log10(psd) )
        plx.plotsize(100,30)
        plx.title("PSD of Sweep Output")
        plx.show()
    

    
    print("saving PSD...")
    
    a = {'transfer_function': psd,
         'transfer_function_freq': freqs
         }

    with open('transfer_function/transfer_function_RPi.pkl', 'wb') as handle:
        pickle.dump(a, handle)
        

    
    return


## function for SCG generation process
def generate_process(z_axis,startRec,doneRec,fileName,output):

    sleep(2)
    
    print(bcolors.OK + 'starting generator' + bcolors.RESET)
        
    cwd=os.getcwd()+"/waves/"
    
    mixer.pre_init(1000,-16,2,1200)
    mixer.init()
    print(f"Initialized: {mixer.get_init()}")
    mixer.set_num_channels(2)
    print(f"Number of channels: {mixer.get_num_channels()}")
    
    sound0=mixer.Sound(cwd+fileName[0]+"_SCG.wav")
    channel0=mixer.Channel(0)
    channel0.set_volume(0.0,0.9)
    
    
    sound1=mixer.Sound(cwd+fileName[0]+"_ECG.wav")
    channel1=mixer.Channel(1)
    channel1.set_volume(0.1 ,0.0)  ## to increase ECG amplitude
    
    channel0.play(sound0)
    channel1.play(sound1)
        
    sleep(4)
    startRec.value=1
    while channel0.get_busy() == True:
        continue
    
    while channel1.get_busy() == True:
        continue
    
    sleep(5)
    
        
    print(bcolors.OK +'done generator'+ bcolors.RESET)
        
    startRec.value=0
    doneRec.value=1
        
    sleep(1)
        
    data=list(z_axis).copy()
        
    data=[float(i)*0.0078*-1 for i in data]
    data=np.asarray(data)
    data=data-np.mean(data)
    #     plt.ion()
    print("Plotting...")
        
    if(fileName[1]=="desktop"):
        #plt.figure()
        #plt.plot(range(len(data)),data)
       # plt.title("Output of Generator")
        #plt.show()
       print('ehhlo')
    else:
        plx.clp()
        plx.plot(range(len(data)),data)
        plx.plotsize(100,30)
        plx.title("Output of Generator")
        plx.show()

    print("calculating FFT...")
        
    SAMPLE_RATE=1000
    N = len(data)

    yf = fft(data)
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    yf= fftshift(yf)
    xf= fftshift(xf)

    if(fileName[1]=="desktop"):
      #  plt.figure()
       # plt.plot(xf[int(len(xf)/2):int(len(xf)/2+N/8)],np.square(np.abs(yf[int(len(xf)/2):int(len(xf)/2+N/8)])))
        #plt.title("FFT")
        #plt.show()
       print('ehhlo')
    else:
        plx.clp()
        plx.plot(xf[int(len(xf)/2):int(len(xf)/2+N/8)],np.square(np.abs(yf[int(len(xf)/2):int(len(xf)/2+N/8)])))
        plx.plotsize(100,30)
        plx.title("FFT")
        plx.show()
        
    nSegments=1
    overlap=0.1
    nPerSeg = np.round(len(data)//nSegments/overlap)
    if nSegments ==1:
        nPerSeg = len(data)
    nOverlap=np.round(overlap*nPerSeg)
        
    NFFT=len(xf)
    freqs, psd = signal.welch(data,SAMPLE_RATE,window='hamm', noverlap=10,detrend='constant', nfft=NFFT, return_onesided=True, scaling='spectrum')
    #     freqs, psd = signal.periodogram(data,SAMPLE_RATE, window='hann', nfft=NFFT,scaling='spectrum')
    psd=psd**0.5
        


    print("Plotting PSD...")
    if(fileName[1]=="desktop"):
       # plt.figure()
       # plt.plot(freqs, 10*np.log10(psd) )
      #  plt.title("PSD of Generator Output")
       # plt.show()
       print('hello')
    else:
        plx.clp()
        plx.plot(freqs, 10*np.log10(psd) )
        plx.plotsize(100,30)
        plx.title("PSD of Generator Output")
        plx.show()
        
        
    #     with cal_data.get_lock():
    output.append(data.copy())
    
    
    return



accel=ADXL355(0,0)

print("hi")
print(hex(accel.spi_read_reg(0x00)))
    
#init adxl355
print("Initializing ADXL355...")
##RANGE
accel.spi_write_reg(0x2C,0x42)
print(f"RANGE: {hex(accel.spi_read_reg(0x2C))}")

##POWER_CTL
accel.spi_write_reg(0x2D,0x02)
print(f"POWER_CTL: {hex(accel.spi_read_reg(0x2D))}")

##FILTER
accel.spi_write_reg(0x28,0x02)
print(f"FILTER: {hex(accel.spi_read_reg(0x28))}")

##Watermark
accel.spi_write_reg(0x29,87)
print(f"Watermark: {accel.spi_read_reg(0x29)}")

##INTERRUPT_MAP
accel.spi_write_reg(0x2A,0x42)
print(f"INTERRUPT_MAP: {hex(accel.spi_read_reg(0x2A))}")

print(bcolors.OK + "Accelerometer sampling rate = 1000 Hz" + bcolors.RESET)


manager = mp.Manager()
z_data=manager.list()
cal_data=manager.list()
fileName=manager.list()
output=manager.list()
startRec=manager.Value('i',0)
doneRec=manager.Value('i',0)

adxlThread=mp.Process(target=adxl_process, args=[z_data,startRec,doneRec])
generateThread=mp.Process(target=generate_process, args=[z_data,startRec,doneRec,fileName, output])
calibrateThread=mp.Process(target=calibrate_process, args=[z_data,startRec,doneRec,cal_data,fileName])
tfEstimateThread=mp.Process(target=tf_estimate_process, args=[z_data,startRec,doneRec,cal_data,fileName])


mode=0
#to run:
# %Run sam_SCG_Generator.py generate (filename) desktop

## user interface and argument handling
try:

    if sys.argv[1]=="generate":
        
        if(len(sys.argv)==4):
            mode=0
           
            fileName.append(sys.argv[2])
            # for above line^^ enter the name of the .wav file to be read into the program.
            # for some reason it appends _SCG.wav onto the written filename
            if sys.argv[3]=="desktop" or sys.argv[3]=="terminal":
                fileName.append(sys.argv[3])
            else:
                print(bcolors.FAIL +"Last argument invalid! [terminal/desktop]!"+ bcolors.RESET)
                exit()
                
            print(bcolors.OK + "Generator mode selected" + bcolors.RESET)
            
        else:
            print(bcolors.FAIL+"Invalid arguments!"+ bcolors.RESET)
            exit()
        
        
    elif sys.argv[1]=="calibrate":
        if(len(sys.argv)==4):
            mode=1
            
            fileName.append(sys.argv[2])
            if sys.argv[3]=="desktop" or sys.argv[3]=="terminal":
                fileName.append(sys.argv[3])
            else:
                print(bcolors.FAIL+"Last argument invalid! [terminal/desktop]!"+ bcolors.RESET)
                exit()
        else:
            print(bcolors.FAIL+"Invalid arguments!"+ bcolors.RESET)
            exit()
            
        print(bcolors.OK + "Calibration mode selected" + bcolors.RESET)
    
    elif sys.argv[1]=="tf_estimate":
        if(len(sys.argv)==3):
            mode=2
            if sys.argv[2]=="desktop" or sys.argv[2]=="terminal":
                fileName.append(sys.argv[2])
            else:
                print(bcolors.FAIL+"Last argument invalid! [terminal/desktop]!"+ bcolors.RESET)
                exit()
        else:
            print(bcolors.FAIL+"Invalid arguments!"+ bcolors.RESET)
            exit()
            
        print(bcolors.OK + "TF estimate mode selected" + bcolors.RESET)

    else:
        print("Invalid arguments!")
        exit()
    
    

    if mode==0:
        if not (os.path.isfile(os.getcwd()+"/waves/"+fileName[0]+"_SCG.wav") and os.path.isfile(os.getcwd()+"/waves/"+fileName[0]+"_ECG.wav")):
            print(f"{os.getcwd()}/waves/{fileName[0]}_SCG.wav File doesn't exist")
            fileName[:]=[]
            
            exit()
            
    adxlThread.daemon=True
    generateThread.daemon=True
    
    adxlThread.start()
    if(mode==0):
        generateThread.start()
    elif(mode==1):
        calibrateThread.start()
    elif(mode==2):
        tfEstimateThread.start()
    
    adxlThread.join()
    if(mode==0):
        generateThread.join()
    elif(mode==1):
        calibrateThread.join()
    elif(mode==2):
        tfEstimateThread.join()
    
    if(mode==0):
        if not os.path.exists('recordings'):
            os.makedirs('recordings')
        
        i=0
        cwd=os.getcwd()
        csvfilename=cwd+"/recordings/"+"output_"+ fileName[0] +'_'+str(i)+".csv"
        while(os.path.isfile(csvfilename)):
            i+=1
            csvfilename=cwd+"/recordings/"+"output_"+ fileName[0]+'_'+str(i)+".csv"
        
        np.savetxt(csvfilename,output[0],delimiter=",")
        print(bcolors.OK + "Saved recording" + bcolors.RESET)
    
    elif(mode==1):
        saveOrnot=input("Save? [y/n] ")
        
        if saveOrnot=='y':
            if not os.path.exists('waves'):
                os.makedirs('waves')
            cwd=os.getcwd() 
            filename=cwd+"/waves/"+input("Enter file name: ")
    
            ECG_audio = np.asarray(cal_data[0])
            SCG_audio = np.asarray(cal_data[1])
            
            


            save_wav(filename,SCG_audio,ECG_audio,sample_rate=1000)
            
    sleep(1)
    print(bcolors.OK + "Done!!" + bcolors.RESET)
    print("Terminating Processes")
    adxlThread.terminate()
    if mode==0:
        generateThread.terminate()
    elif(mode==1):
        calibrateThread.terminate()
    elif(mode==2):
        tfEstimateThread.terminate()
    
    adxlThread.close()
    if mode==0:
        generateThread.close()
    elif(mode==1):
        calibrateThread.close()
    elif(mode==2):
        tfEstimateThread.close()
        
    
    z_data[:]=[]
    exit()

        
except KeyboardInterrupt:
    print(bcolors.FAIL + "\n-------Keyboard interrupt!!---------" + bcolors.RESET)
    print(bcolors.FAIL + "======Terminating Processes====="+ bcolors.RESET)
#     os.system('killall "omxplayer.bin"')
    if(mixer.music.get_busy==True):
        mixer.music.fadeout(1000)
    
    adxlThread.terminate()
    if mode==0:
        generateThread.terminate()
    elif(mode==1):
        calibrateThread.terminate()
    elif(mode==2):
        tfEstimateThread.terminate()
        
    sleep(1)
    
    adxlThread.close()
    if mode==0:
        generateThread.close()
    elif(mode==1):
        calibrateThread.close()
    elif(mode==2):
        tfEstimateThread.close()
        
    exit()


                                                                                                   

