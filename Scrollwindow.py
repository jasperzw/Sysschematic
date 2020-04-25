import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
#test
scrollbar_y = ttk.Scrollbar(container, orient="vertical",command=canvas.yview)
scrollbar_x = ttk.Scrollbar(container, orient="horizontal",command=canvas.xview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
#test
canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar_y.set)
canvas.configure(xscrollcommand=scrollbar_x.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()
container.pack()
canvas.pack(side="top", fill="both", expand = True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")

root.mainloop()


#####
class AutoScrollbar(Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise TclError('Cannot use place with this widget')

class Zoom(Frame):
    ''' Simple zoom with mouse wheel '''
    def __init__(self, mainframe, path):
        ''' Initialize the main Frame '''
        Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.draw = Canvas(canvas, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.draw.grid(row=1, sticky='nswe')
        vbar.configure(command=self.draw.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.draw.xview)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.draw.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        # Show image and plot some random test rectangles on the canvas
        # Text is used to set proper coordinates to the image. You can make it invisible.
        self.text = self.canvas.create_text(0, 0, anchor='nw', text='Scroll to zoom')
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
Zoom(master, path = canvas)
