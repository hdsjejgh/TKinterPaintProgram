import tkinter as tk
from tkinter import ttk,colorchooser

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.menubar = tk.Menu(self.root)

        self.file = tk.Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File",menu=self.file)
        self.file.add_command(label="Save",command=print)
        self.file.add_command(label="Exit",command=self.__exit)

        self.edit = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.edit)
        self.edit.add_command(label="Undo", command=self.__undo)

        self.canvas = tk.Canvas(self.root,width=500,height=500,bg="White")
        self.canvas.place(x=0,y=0)
        self.canvas.bind('<B1-Motion>',self.__draw)
        self.canvas.bind('<ButtonRelease-1>', self.__clearPrev)

        self.title = tk.Label(text="Sketchpad",width=10,font=("Times New Roman",25),bg="LightGrey")
        self.title.place(x=510,y=10)

        self.root.config(menu=self.menubar)
        self.root.geometry("700x505")
        self.root.resizable(height=False,width=False)
        self.root.title("Sketchpad")
        self.root.bind("<Control-z>",self.__undo)

        self.tool="Line"
        self.size=10
        self.color="Black"
        self.prevX=None
        self.prevY=None
        self.toolsChoices = ("Line","Circle","Square")
        self.toolDD = ttk.Combobox(self.root,values=self.toolsChoices,state="readonly")
        self.toolDD.bind("<<ComboboxSelected>>",self.__submitTool)
        self.toolDD.current(0)
        tk.Label(self.root,text="Brush: ",font=("Times New Roman",15)).place(x=575,y=70)
        self.toolDD.place(x=530,y=100)

        tk.Label(self.root,text="Select Color: ",font=("Times New Roman",15)).place(x=530,y=150)
        self.colorDisplay=tk.Button(self.root,command=self.__colorSelect,width=2,bg=self.color)
        self.colorDisplay.place(x=650,y=150)

    def Run(self):
        self.root.mainloop()
    def __exit(self):
        self.root.quit()
    def __draw(self,x):
        if self.tool=="Circle":
            self.canvas.create_oval(x.x-self.size/2,x.y-self.size/2,x.x+self.size/2,x.y+self.size/2,fill=self.color,outline=self.color)
        elif self.tool=="Line":
            if self.prevX is None:
                self.prevX,self.prevY=x.x,x.y
            else:
                self.canvas.create_line(self.prevX,self.prevY,x.x,x.y,fill=self.color)
            self.prevX, self.prevY = x.x, x.y
        elif self.tool=="Square":
            self.canvas.create_rectangle(x.x-self.size/2,x.y-self.size/2,x.x+self.size/2,x.y+self.size/2,fill=self.color,outline=self.color)
        else:
            self.tool="Line"

    def __clearPrev(self,x):
        self.prevY,self.prevX=None,None
    def __submitTool(self,x):
        self.tool=self.toolDD.get()
    def __undo(self,x=5.35):
        items=self.canvas.find_all()
        if items:
            self.canvas.delete(items[-1])
    def __colorSelect(self):
        self.color=colorchooser.askcolor(title="Select Color")[-1]
        self.colorDisplay.config(bg=self.color)

if __name__ == '__main__':
    p=PaintApp()
    p.Run()