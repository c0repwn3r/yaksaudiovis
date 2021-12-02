#
# analysis.py
# Written with <3 by core
#
# Copyright (c) 2021 core
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter, sleep
import math
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
_file = filedialog.askopenfilename()
print('importing wav data', end='\r')
start_time = perf_counter()
samplerate, data = wavfile.read(_file)
print(f'imported in {perf_counter() - start_time} seconds')
length = data.shape[0] / samplerate
print(f'length: {length} seconds')
time = np.linspace(0., length, data.shape[0])
npdata = data
data = data.tolist()
left, right = [], []
start_time = perf_counter()
print(f'splitting: 0/{len(data)}', end='\r')
for index, val in enumerate(data):
    print(f'splitting: {index}/{len(data)}', end='\r')
    left.append(val)
    #right.append(val[1])
print(f'split {len(data)} entries in {perf_counter() - start_time} seconds')

peak_left = [max(left)] * len(left)
min_left = [min(left)] * len(left)
#peak_right = [max(right)] * len(right)

peak_valley_count = len([left[idx] for idx in range(1, len(left) - 1) if left[idx + 1] >
           left[idx] < left[idx - 1] or left[idx + 1] < left[idx] > left[idx - 1]])
print(f'peak/valley count: {peak_valley_count}')

rms = [20 * math.log10(abs(peak_left[0]))] * len(left)
print(rms[0])

plt.plot(time, npdata[:], label="Audio data")
plt.plot(time, peak_left, label="Peak")
plt.plot(time, rms, label="Reference dB")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()