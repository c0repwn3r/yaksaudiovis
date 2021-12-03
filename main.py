#
# main.py
# Written with <3 by c0repwn3r
#
# Copyright (c) 2021 c0repwn3r
#
import os

import logger
import lolcat
import tkinter as tk
from tkinter import ttk
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter, sleep
import math
import easygui

logger = logger.Logger('MainThread', logger.LogLevel.DEBUG)  # Setup main thread logger

lolcat.print_header()  # Print Yaks header

logger.debug('Logging initialized successfully')
logger.debug('Preparing initial state')

lolcat.run('Welcome to yaksaudiovis! Please wait while the program initializes.')
lolcat.reset()

# +--------------------------+
# | Audio analysis variables |
# +--------------------------+
sample_size = 0.025  # Audio sample size in seconds
average_peak_count = 50  # Amount of peaks to average together

logger.info('Initialized audio analysis module to default values')

# +---------------+
# | Tkinter setup |
# +---------------+

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Responsive!
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.enable_peakcount = tk.BooleanVar(value=True)
        self.enable_average = tk.BooleanVar(value=True)

        self.show_plot = tk.BooleanVar(value=True)
        self.show_results = tk.BooleanVar(value=True)

        self.file_location = tk.StringVar()

        self.progress_var = tk.DoubleVar(value=0.0)
        self.task_progress_var = tk.DoubleVar(value=0.0)

        # Create widgets
        self.options_frame = ttk.LabelFrame(self, text="Options", padding=(20, 10)) # Frame to contain options
        self.options_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nswe"
        )

        # Options
        self.peakcount_chk = ttk.Checkbutton(
            self.options_frame, text="Enable peak count", variable=self.enable_peakcount, command=self.reevaluate_options
        )
        self.peakcount_chk.grid(row=0, column=0, padx=5, pady=10, sticky="nswe")

        self.average_chk = ttk.Checkbutton(
            self.options_frame, text="Enable average vol.", variable=self.enable_average, command=self.reevaluate_options
        )
        self.average_chk.grid(row=1, column=0, padx=5, pady=10, sticky="nswe")

        self.plot_chk = ttk.Checkbutton(
            self.options_frame, text="Show plot", variable=self.show_plot,
            command=self.reevaluate_options
        )
        self.plot_chk.grid(row=2, column=0, padx=5, pady=10, sticky="nswe")

        self.result_chk = ttk.Checkbutton(
            self.options_frame, text="Show results", variable=self.show_results,
            command=self.reevaluate_options
        )
        self.result_chk.grid(row=3, column=0, padx=5, pady=10, sticky="nswe")

        # Control
        self.files = ttk.LabelFrame(self, text="Control", padding=(20, 10))  # Frame to contain options
        self.files.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nswe"
        )

        self.file_location_entry = ttk.Entry(self.files, textvariable=self.file_location)
        self.file_location_entry.insert(0, 'Input path')
        self.file_location_entry.grid(
            row=0, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.file_location_entry.bind('<Double-Button-1>', self.select_file)
        self.file_location.trace_add('write', self.reevaluate_options)

        self.go_btn = ttk.Button(self.files, text="Go!", style="Accent.TButton", command=self.go)
        self.go_btn.grid(
            row=1, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.label = ttk.Label(
            self.files,
            text="0/7 Ready",
            justify="center",
            font=("-size", 12)
        )
        self.label.grid(
            row=2, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.progress = ttk.Progressbar(
            self.files, value=0, variable=self.progress_var, mode="determinate", maximum=6
        )
        self.progress.grid(
            row=3, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.task_progress = ttk.Progressbar(
            self.files, value=0, variable=self.task_progress_var, mode="determinate", maximum=100
        )
        self.task_progress.grid(
            row=4, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.reevaluate_options()

    def set_progress(self, msg, amt):
        self.task_progress['maximum'] = 7
        self.progress_var.set(amt)
        self.label['text'] = str(amt) + '/7 ' + msg

        window.update_idletasks()

    def set_task_progress(self, amt):
        self.task_progress_var.set(amt)
        window.update_idletasks()
        window.update()

    def reevaluate_options(self, a=None, b=None, c=None, d=None):
        to_do = True
        good_file = True
        if not self.show_plot.get() and not self.show_results.get():
            to_do = False
        else:
            to_do = True
        if not os.path.exists(self.file_location.get()):
            good_file = False
        else:
            good_file = True
        if not to_do:
            self.set_progress('Nothing to do', 0)
            self.go_btn['state'] = 'disabled'
        elif not good_file:
            self.set_progress('Invalid file', 0)
            self.go_btn['state'] = 'disabled'
        else:
            self.set_progress('Ready', 0)
            self.go_btn['state'] = 'normal'

    def select_file(self, smth):
        _file = easygui.fileopenbox()
        self.file_location.set(_file)
        self.reevaluate_options()

    def go(self):
        # 0/7 Ready
        # 1/7 Rebuilding fontcache
        # 2/7 Importing audio
        # 3/7 Reading metadata
        # 4/7 Mapping in timespace
        # 5/7 Transposing data
        # 6/7 Analyzing
        # 7/7 Done
        analysis_start_time = perf_counter()
        logger.info('Starting analysis')
        self.set_progress('Validating input', 0)
        file_loc = self.file_location.get()
        logger.debug('Checking for valid file path')

        if not os.path.exists(file_loc):
            logger.error('Invalid or nonexistent input path')
            self.set_progress('Invalid input file', 0)
            return

        logger.info('Triggering matplotlib fontcache rebuild')
        self.set_progress('Rebuilding fontcache', 1)

        logger.info('Importing audio')
        self.set_progress('Importing audio', 2)

        start_time = perf_counter()
        samplerate, data = wavfile.read(file_loc)
        logger.debug(f'Samplerate: {samplerate}')
        logger.warn('Ignore the WavFileWarning, it\'s caused by WAV metadata that scipy can\'t understand')
        logger.info(f'Imported audio file from {file_loc} in {perf_counter() - start_time} seconds')

        self.set_progress('Importing metadata', 3)
        logger.info('Reading additional info from file')

        length = data.shape[0] / samplerate

        self.set_progress('Mapping to timespace', 4)
        logger.info('Executing npinspace')

        time = np.linspace(0., length, data.shape[0])
        npdata = data
        data = data.tolist()
        left, right = [], []

        self.set_progress('Transposing data', 5)
        logger.info('Transposing data')

        start_time = perf_counter()

        total = len(data)
        self.task_progress['maximum'] = total
        p = 0
        for index, val in enumerate(data):
            if p == 50:
                self.set_task_progress(index)
                p = 0
            p += 1
            left.append(val)

        logger.debug(f'Transposed {total} frames in {perf_counter() - start_time} seconds')

        self.set_progress('Analyzing data', 6)

        peak_left = [max(left)] * len(left)

        if self.enable_peakcount.get():
            peak_valley_count = len([left[idx] for idx in range(1, len(left) - 1) if left[idx + 1] >
                                 left[idx] < left[idx - 1] or left[idx + 1] < left[idx] > left[idx - 1]])
            logger.info(f'Peak/valley count: {peak_valley_count}')

        rms = [20 * math.log10(abs(peak_left[0]))] * len(left)
        logger.info(f'RMS volume level: {rms[0]}')

        if self.show_results.get():
            popup = tk.Toplevel(window)
            popup.title('Results')
            tk.Label(popup, text=f'RMS Volume: {round(rms[0], 3)}').pack()
            if self.enable_peakcount.get():
                tk.Label(popup, text=f'Peak count: {peak_valley_count}').pack()
            tk.Label(popup, text=f'Audio length: {round(length, 2)}s').pack()
            tk.Label(popup, text=f'Entries: {total}').pack()
            tk.Label(popup, text=f'Samplerate: {samplerate}').pack()
            if self.enable_average.get():
                tk.Label(popup, text=f'Average: {sum(data) / len(data)}').pack()

        rtime = perf_counter() - analysis_start_time
        rtime = round(rtime, 3)
        self.set_progress(f'Done ({rtime}s)', 7)
        self.set_task_progress(0)

        logger.info(f'Finished analysis in {rtime}s')

        if self.show_plot.get():
            plt.plot(time, npdata[:], label="Audio data")
            plt.plot(time, peak_left, label="Peak")
            plt.plot(time, rms, label="Reference dB")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.show()


logger.info('Creating window')
window = tk.Tk()

logger.debug('Setting window title to yaksaudiovis')
window.title('YaksAudioVis')

logger.debug('Setting window theme to Azure (credit goes to rdbende, <3)')
window.tk.call('source', 'azure.tcl')
window.tk.call('set_theme', 'dark')

logger.debug('Starting app')
app = App(window)
app.pack(fill="both", expand=True)

# Set a minsize for the window and place it in the middle
window.update()
window.minsize(window.winfo_width(), window.winfo_height())
x_coordinate = int((window.winfo_screenwidth() / 2) - (window.winfo_width() / 2))
y_coordinate = int((window.winfo_screenheight() / 2) - (window.winfo_height() / 2))
window.geometry("+{}+{}".format(x_coordinate, y_coordinate-20))

logger.info('Setup completed! Opening window')
window.mainloop()
