from tkinter import *

reloadStatus = 0

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

class Zoom_Advanced(Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe):
        ''' Initialize the main Frame '''
        Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = mainframe
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.update()  # wait till canvas is created
        self.textSize = 2
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-4>', self.wheel)
        self.canvas.bind('<Button-5>', self.wheel)
        self.canvas.bind('i',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('o',   self.wheel)  # only with Linux, wheel scroll up
        self.delta = 0.75  # zoom magnitude
        #self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.currentZoom = 1
        # Put image into container rectangle and use it to set proper coordinates to the image
    #    self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # Plot some optional random rectangles for the test purposes

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
#        bbox = self.canvas.bbox(self.container)  # get image area
#        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
#        else: return  # zoom only inside image area
        scale = 1.0
#         Respond to Windows (event.delta) wheel event
        if event.delta == -120 or event.num == 5:  # scroll down

            #if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            scale        *= self.delta
        if event.delta == 120 or event.num == 4:  # scroll up
            #i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            #if i < self.imscale: return  # 1 pixel is bigger than the visible area
            scale        /= self.delta

        self.currentZoom *= scale
        roundedTextSize = round(self.textSize*self.currentZoom)
        if(roundedTextSize < 1):
            roundedTextSize = 1
        #print("current text size: ", roundedTextSize)
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        wNotList = self.canvas.find_withtag("wNotation")
        for x in wNotList:
            self.canvas.itemconfig(x,font=("Courier", roundedTextSize))


        #self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        #print('the current used scale: ', self.currentZoom, " with delta adjusment: ",scale)

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="enter the external or noise source")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def reloadCall(subMenu,reload,currentAmountOutputSelected,selectedNode):
    global reloadStatus
    #print(reloadStatus)
    #print(currentAmountOutputSelected)
    if((currentAmountOutputSelected == 1 or currentAmountOutputSelected > 2) and reloadStatus == 1):
        print("removing the select window")
        for x in reload:
            x.pack_forget()
        reloadStatus = 0
    elif(currentAmountOutputSelected == 2 and reloadStatus == 0):
        print("loading in the select window")
        #print("node: ",selectedNode.nmb)
        for x in range(8):
            reload[x].pack(padx=2, pady=2)
        for x in range(5):
            x += 8
            print(selectedNode.nodeMode[x-10].get())
            reload[x].configure(variable=selectedNode.nodeMode[x-10])
            reload[x].pack(padx=2, pady=2)
        reloadStatus = 1
