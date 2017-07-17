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
    
def play(pattern, loops=3):
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

# Examples

playlist={
    'conga':E(2,3),
    'take5':E(2,5),
    'biao':E(3,4),
    'sangsa':E(3,5),
    'money':E(3,7),
    'tresillo':E(3,8),
    'savari_tal':E(3,11),
    'dhamar_tal':E(3,14),
    'mirena':E(4,5),
    'ruchenitza':E(4,7),
    'asak':E(4,9),
    'outside_now':E(4,11),
    'pancam_savarı_tal':E(4,15),
    'york_samai':E(5,6),
    'nawakhat':E(5,7),
    'cinquillo':E(5,8),
    'agsag_samai':E(5,9),
    'pictures_at_an_exhibition':E(5,11),
    'chakacha':E(5,12),
    'macedonian_1':E(5,13),
    'bossa_nova':E(5,16),
    'pontakos':rotate(E(6,7),5),
    'mama_cone_pita':E(6,13),
    'bendir':rotate(E(7,8),6),
    'bazaragana':E(7,9),
    'lenk_fahhte':E(7,10),
    'yoruba':E(7,12),
    'bulgarian_1':rotate(E(7,13),2),
    'samba':E(7,16),
    'macedonian_2':rotate(E(7,17),3),
    'bulgarian_2':E(7,18),
    'bulgarian_3':E(8,17),
    'bulgarian_4':rotate(E(8,19),3),
    'tsofyan':rotate(E(9,14),2),
    'luba':rotate(E(9, 16),2),
    'bulgarian_5':rotate(E(9, 22),2),
    'bulgarian_6':E(9,23),
    'sot_silam':rotate(E(11,12),1),
    'aka_1':E(11,24),
    'aka_2':E(13,24),
    'bulgarian_7':rotate(E(15,34),32)
    }
