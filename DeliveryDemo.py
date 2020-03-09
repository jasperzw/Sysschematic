# Importing tkinter module 
from tkinter import *
  
#een simpele functie waarmee het makkelijker wordt om circkels te maken
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def draw_example(w,x,y):
    w.create_line(100+x, 265+y, 180+x, 265+y, arrow=LAST)
    w.create_line(220+x, 265+y, 300+x, 265+y, arrow=LAST)

    w.create_line(310+x, 270+y, 310+x, 350+y)
    w.create_line(310+x, 350+y, 220+x, 350+y, arrow = LAST)

    w.create_line(110+x, 275+y, 110+x, 350+y, arrow=FIRST)
    w.create_line(180+x, 350+y, 110+x, 350+y)

    w.create_line(50+x, 265+y, 100+x, 265+y, arrow = LAST)
    w.create_line(310+x, 265+y, 350+x, 265+y, arrow = LAST)

    w.create_circle(200+x,270+y,20)
    w.create_text(200+x,270+y,text="w")
    w.create_circle(200+x,350+y,20)
    w.create_text(200+x,350+y,text="w")

    b1 = Button(master, text = "G1", bg = "cyan", command=lambda : module_call('G1')) 
    b1_view = w.create_window(110+x, 265+y, window=b1)

    b2 = Button(master, text = "G2", bg = "cyan", command=lambda : module_call('G2')) 
    b2_view = w.create_window(310+x, 265+y, window=b2)

def initialize_display(w):
    m1 = Button(master, text = "Load .mat file") 
    m1_view = w.create_window(50,20, window=m1)
    m2 = Button(master, text = "Load example", command=lambda : draw_example(w,300,200) )
    m2_view = w.create_window(50,50, window=m2)
    m3 = Button(master, text = "Clear canvas", command=lambda : clear_canvas(w))
    m3_view = w.create_window(50,80, window=m3)
    w.create_text(900,10,text="The current value is:")

def module_call(module_name):
    w.create_text(965,10,text=module_name)

def clear_canvas(w):
    w.delete('all')
    initialize_display(w)

# creating Tk window 
master = Tk() 
  
# setting geometry of tk window 

master.title("Delivery Demo")

# canvas aanmaken en even een proef of concept hardcode op het scherm
w = Canvas(master, width=1000, height=600)
w.pack()
initialize_display(w)

  
# label widget 
# infinite loop which is required to 
# run tkinter program infinitely 
# until an interrupt occurs 
mainloop() 