import tkinter as tk

class Excel(tk.Frame):
    def __init__(self, master, rows, columns, width):
        super().__init__(master)

        for i in range(columns):
            self.make_entry(0, i+1, width, f'W{i}', False)

        for row in range(rows):
            self.make_entry(row+1, 0, 5, f'W{row}', False)

            for column in range(columns):
                self.make_entry(row+1, column+1, width, '', True)

    def make_entry(self, row, column, width, text, state):
        e = tk.Entry(self, width=width)
        if text: e.insert(0, text)
        e['state'] = tk.NORMAL if state else tk.DISABLED
        e.coords = (row-1, column-1)
        e.grid(row=row, column=column)

    def show_cells():
        print('\n--== dumping cells ==--')
        print(ex.children.get())

def loadMatrixEditor(master):

    call = popupWindow(master)
    master.wait_window(call.top)

    #ex = Excel(app, rows=5, columns=10, width=8)
    #ex.pack(padx=20, pady=20)

    #bt = tk.Button(app, text='Dump', command=show_cells)
    #bt.pack(pady=20)
