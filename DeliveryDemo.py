# Importing tkinter module 
from tkinter import *
from exampleLib import *
  
#A simple function to draw circles in a canvas
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


#initializes the main menu. you have to pass the mainmenu frame and the canvas so that it could pass the canvas id when clearing it
def initMainMenu(frame, canvas):

    #column 0
    Button(frame, text="load .mat file", height = 1, width=20).grid(row=0, padx=2, pady=2)
    Button(frame, text="export .mat file", height = 1, width=20).grid(row=1, padx=2, pady=2)
    Button(frame, text="load example network", command= lambda: draw_example(draw,-10, -150,master), height = 1, width=20).grid(row=2, padx=2, pady=2)

    #column 1
    Button(frame, text="Options", height = 1, width=20).grid(row=0, column=1, padx=2, pady=2)
    Button(frame, text="Go to global veiw", height = 1, width=20).grid(row=1, column=1, padx=2, pady=2)
    Button(frame, text="Clear window", command= lambda: clearWindow(canvas), height = 1, width=20).grid(row=2, column=1, padx=2, pady=2)

#same as main menu initializes the submenu
def initSubMenu(frame):
    Label(frame, text="currently selected:", bg="gray").pack()
    Button(frame, text="Remove node", height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="View internals", height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Make known", height = 1, width=20).pack(padx=2, pady=2)

def clearWindow(canvas):
    canvas.delete("all")

# creating Tk window 
master = Tk() 
master.configure(background="gray")
  

#seperating the menu in different frames which will hold all the components so that it is easier to use .grid for button placemant
master.title("Delivery Demo")
mainMenu = Frame(master, bg="gray")
canvas = Frame(master, bg="white")
subMenu = Frame(master, bg="gray")

#alligning the grid
mainMenu.grid(row=0, sticky=NW)
canvas.grid(row=1)
subMenu.grid(row=0, column=1, rowspan=2, sticky=NE)

draw = Canvas(canvas, height=300, width=500, bg="white")
draw.pack()
initMainMenu(mainMenu, draw)
initSubMenu(subMenu)


# canvas aanmaken en even een proef of concept hardcode op het scherm
#w = Canvas(master, width=1000, height=600)
#w.pack()
#initialize_display(w,master)

  
# label widget 
# infinite loop which is required to 
# run tkinter program infinitely 
# until an interrupt occurs 
mainloop() 