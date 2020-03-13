from tkinter import *

def draw_example(w,x,y,master):
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

    b1 = Button(master, text = "G1", bg = "cyan", command=lambda : module_call('G1',w, master)) 
    b1_view = w.create_window(110+x, 265+y, window=b1)

    b2 = Button(master, text = "G2", bg = "cyan", command=lambda : module_call('G2',w,master)) 
    b2_view = w.create_window(310+x, 265+y, window=b2)

def module_call(module_name,w,master):
    w.create_text(965,10,text=module_name)

def initialize_display(w,master):
    m1 = Button(master, text = "Load .mat file") 
    m1_view = w.create_window(50,20, window=m1)
    m2 = Button(master, text = "Load example", command=lambda : draw_example(w,300,200, master) )
    m2_view = w.create_window(50,50, window=m2)
    m3 = Button(master, text = "Clear canvas", command=lambda : clear_canvas(w,master))
    m3_view = w.create_window(50,80, window=m3)
    w.create_text(900,10,text="The current value is:")

def clear_canvas(w,master):
    w.delete('all')
    initialize_display(w,master)


