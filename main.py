#
# main.py
# Written with <3 by c0repwn3r
#
# Copyright (c) 2021 c0repwn3r
#
import logger
import lolcat
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib
from matplotlib import font_manager

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

        self.custom_sample_size = tk.BooleanVar(value=False)
        self.use_stereo = tk.BooleanVar(value=False)

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

        self.custom_sample_size_chk = ttk.Checkbutton(
            self.options_frame, text="Custom sample size", variable=self.custom_sample_size, command=self.reevaluate_options
        )
        self.custom_sample_size_chk.grid(row=2, column=0, padx=5, pady=10, sticky="nswe")

        self.use_stereo_chk = ttk.Checkbutton(
            self.options_frame, text="Analyze both channels", variable=self.custom_sample_size,
            command=self.reevaluate_options
        )
        self.use_stereo_chk.grid(row=2, column=0, padx=5, pady=10, sticky="nswe")

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

        self.go_btn = ttk.Button(self.files, text="Go!", style="Accent.TButton", command=self.go)
        self.go_btn.grid(
            row=1, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.label = ttk.Label(
            self.files,
            text="0/9 Ready",
            justify="center",
            font=("-size", 15, "-weight", "bold")
        )
        self.label.grid(
            row=2, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.progress = ttk.Progressbar(
            self.files, value=0, variable=self.progress_var, mode="determinate", length=6
        )
        self.progress.grid(
            row=3, column=0, padx=5, pady=10, sticky="nswe"
        )

        self.task_progress = ttk.Progressbar(
            self.files, value=0, variable=self.task_progress_var, mode="determinate", length=0
        )
        self.task_progress.grid(
            row=4, column=0, padx=5, pady=10, sticky="nswe"
        )

    def reevaluate_options(self):
        if not self.enable_average and not self.enable_peakcount:
            self.go_btn['state'] = 'disabled'
            return
        self.go_btn['state'] = 'enabled'

    def select_file(self, smth):
        root = tk.Tk()
        root.withdraw()
        _file = filedialog.askopenfilename()
        self.file_location.set(_file)

    def set_progress(self, msg, amt):
        self.progress_var.set(amt / 6)
        self.label['text'] = msg
        window.update_idletasks()
        self.update_idletasks()
        self.update()
        window.update()

    def set_task_progress(self, amt, total):
        self.task_progress['length'] = total
        self.task_progress_var.set(amt / total)
        window.update_idletasks()
        self.update_idletasks()
        self.update()
        window.update()

    def go(self):
        self.set_progress('Updating font cache', 1)
        self.set_progress('Importing audio data', 2)


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
