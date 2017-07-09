import random
import math
import time
import numpy
import pygame
from pygame.locals import *

def click(T,sampling_rate):
    return([.75+.25*random.random() for i in range(int(round(T*sampling_rate)))])

def rhythm(pattern, duration, sampling_rate, T, bits):
    beat = duration/len(pattern)
    clk = click(min(T,beat),sampling_rate)
    n_samples = max(len(pattern)*len(clk), int(round(duration*sampling_rate)))
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(bits - 1) - 1
    j=0
    for i in pattern:
        if i==1:
            n = j*len(clk)
            for k in range(len(clk)):
                buf[n+k][0]=int(round(max_sample*clk[k]))
                buf[n+k][1]=buf[j+k][0]
        j=j+1
    return(pygame.sndarray.make_sound(buf))

    
def play(pattern, reps=0):
    size = (1366, 720)
    bits = 16
    duration = len(pattern)/10.0          # in seconds
    sampling_rate = 44100
    pygame.mixer.pre_init(sampling_rate, -bits, 2)
    pygame.init()
    snd = rhythm(pattern,duration,sampling_rate,0.2,bits)
    snd.play(reps)
