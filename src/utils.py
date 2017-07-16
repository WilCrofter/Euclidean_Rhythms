import random
import math
import numpy
import pygame
from pygame.locals import *

def drum(T,sampling_rate,f,a):
    tend = 2*math.log(10)/a
    nend = int(round(tend*sampling_rate))
    nsamp = int(round(T*sampling_rate))
    ans = [0.0 for i in range(nsamp)]
    for i in range(nend):
        t = i/sampling_rate
        ans[i%nsamp] +=  math.exp(-a*t)*math.sin(2*math.pi*f*t)
    return(ans)
    
def rhythm(pattern, duration, sampling_rate, T, bits):
    beat = duration/len(pattern)
    clk = drum(min(T,beat),sampling_rate, 220.0, 2*math.log(10)/T)
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
    
def play(pattern, loops=5):
    size = (1366, 720)
    bits = 16
    duration = len(pattern)/10.0          # in seconds
    sampling_rate = 44100
    pygame.mixer.pre_init(sampling_rate, -bits, 2)
    pygame.init()
    snd = rhythm(pattern,duration,sampling_rate,0.2,bits)
    snd.play(loops)

def Bjorklund(k,n):
    if not type(k) == type(n) == int:
        raise TypeError('Arguments must be integers.')
    if not n > k:
        raise ValueError('Second argument must exceed the first.')
    tmp = [[1] for i in range(k)] + [[0] for i in range(n-k)]
    while ([0] in tmp) or (len(tmp) > 1):
        idx = tmp.index(tmp[-1])
        if len(tmp) == 1+idx:
            break
        for i in range(min(idx,len(tmp)-idx)):
            tmp[i] += tmp[-1]
        tmp = tmp[0:max(idx,len(tmp)-idx)]
    ans = []
    for i in range(len(tmp)):
        ans += tmp[i]
    return(ans)

# Aliases:

bjorklund = Bjorklund
E = Bjorklund

def onsets(pattern):
    return([i for i,x in enumerate(pattern) if x==1])

def rotate(pattern, k):
    if not type(k) == int:
        raise TypeError('Second argument must be an integer')
    n = len(pattern)
    k = k%n
    return(pattern[k:n]+pattern[0:k])

def geodesics(pattern):
    ons = onsets(pattern)
    n = len(pattern)
    ans=[(ons[i]-ons[j])%n for i in range(len(ons)) for j in range(i)]
    ans.sort()
    return(ans)

