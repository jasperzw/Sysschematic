from tkinter import *

class Excel(Frame):
    def __init__(self, master, rows, columns, width):
        super().__init__(master)
        self.col = columns
        self.row = rows

        for i in range(columns):
            self.make_entry(0, i+1, width, f'W{i}', False)

        for row in range(rows):
            self.make_entry(row+1, 0, 5, f'W{row}', False)

            for column in range(columns):
                self.make_entry(row+1, column+1, width, 1, True)

    def make_entry(self, row, column, width, text, state):
        e = Entry(self, width=width)
        if text: e.insert(0, text)
        e['state'] = NORMAL if state else DISABLED
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)

    def show_cells(self):
        buckets = [[0 for col in range(self.col)] for row in range(self.row)]
        print('\n--== dumping cells ==--')
        i = 0
        j = 0
        w = self.col
        #print("i:",i,"w:",w,"col:",self.col)
        for e in self.children:
            v = self.children[e]
            #print(f'{v.get()}', end=', ')
            if(j>0 and i>0):
                #print("j:",j,"i:",i)
                buckets[j-1][i-1] = int(v.get())
            i = i+1
            if((i==w and j==0) or (i==w+1 and j>0)):
                #print("")
                j = j+1
                i = 0
        for x in buckets:
            print(x)

class matrixWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Matrix editor")
        self.l.pack()
        self.ex = Excel(top, rows=5, columns=10, width=8)
        self.ex.pack(padx=20, pady=20)
        print(self.ex.col)
        self.bt = Button(top, text='Dump', command=self.ex.show_cells)
        self.bt.pack(pady=20)
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

def loadMatrixEditor(master):

    call = matrixWindow(master)
    master.wait_window(call.top)

    #ex = Excel(app, rows=5, columns=10, width=8)
    #ex.pack(padx=20, pady=20)

    #bt = tk.Button(app, text='Dump', command=show_cells)
    #bt.pack(pady=20)
