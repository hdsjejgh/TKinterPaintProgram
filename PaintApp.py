import tkinter as tk
from tkinter import ttk,colorchooser

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.menubar = tk.Menu(self.root)

        self.file = tk.Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File",menu=self.file)
        self.file.add_command(label="Save",command=self.__save)
        self.file.add_command(label="Exit",command=self.__exit)

        self.edit = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.edit)
        self.edit.add_command(label="Undo", command=self.__undo)
        self.edit.add_command(label="Undo x10", command=self.__uundo)
        self.edit.add_command(label="Clear", command=self.__clear)

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
        self.root.bind("<Control-Z>", self.__uundo)

        self.tool="Pen"
        self.size=10
        self.color="Black"
        self.prevX=None
        self.prevY=None
        self.toolsChoices = ("Pen","Circle","Square")
        self.toolDD = ttk.Combobox(self.root,values=self.toolsChoices,state="readonly")
        self.toolDD.bind("<<ComboboxSelected>>",self.__submitTool)
        self.toolDD.current(0)
        tk.Label(self.root,text="Brush: ",font=("Times New Roman",15)).place(x=575,y=70)
        self.toolDD.place(x=530,y=100)
        self.sizeScale = tk.Scale(self.root, from_=1,to=100,orient="horizontal",length=100,command=self.__sizeSelect)
        self.sizeScale.set(5)
        self.sizeScale.place(x=600-(100/2),y=220)
        tk.Button(self.root,text="+",width=2,relief="groove",command=self.__sizei).place(x=660,y=235)
        tk.Button(self.root, text="-", width=2, relief="groove", command=self.__sized).place(x=523, y=237)
        tk.Label(self.root,text="Change Brush Size: ",font=("Times New Roman",15)).place(x=525,y=200)

        tk.Button(self.root,text="Undo",command=self.__undo,relief="groove").place(x=525,y=327)
        tk.Button(self.root, text="Undo x10", command=self.__uundo,relief="groove").place(x=600, y=340,anchor="center")
        tk.Button(self.root, text="Clear", command=self.__clear,relief="groove").place(x=635, y=327)


        tk.Label(self.root,text="Select Color: ",font=("Times New Roman",15)).place(x=530,y=150)
        self.colorDisplay=tk.Button(self.root,command=self.__colorSelect,width=2,bg=self.color,relief="groove")
        self.colorDisplay.place(x=650,y=150)

        tk.Label(self.root, text="BG Color: ", font=("Times New Roman", 15)).place(x=540, y=285)
        self.bgcDisplay = tk.Button(self.root, command=self.__bgcSelect, width=2, bg="White",relief="groove")
        self.bgcDisplay.place(x=640, y=285)
        icon = tk.PhotoImage("output-onlinepngtools (7).ico")
        self.root.iconbitmap(icon)
    def Run(self):
        self.root.mainloop()
    def __exit(self):
        self.root.quit()
    def __draw(self,x):
        if self.tool=="Circle":
            self.canvas.create_oval(x.x-self.size/2,x.y-self.size/2,x.x+self.size/2,x.y+self.size/2,fill=self.color,outline=self.color)
        elif self.tool=="Pen":
            if self.prevX is None:
                self.prevX,self.prevY=x.x,x.y
            else:
                self.canvas.create_line(self.prevX,self.prevY,x.x,x.y,fill=self.color,width=self.size)
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
    def __uundo(self,x=5.35):
        items=self.canvas.find_all()
        if len(items)>=10:
            for i in range(10):
                self.canvas.delete(items[-1])
                items = self.canvas.find_all()
        else:
            for i in range(len(items)):
                self.canvas.delete(items[-1])
                items = self.canvas.find_all()
    def __colorSelect(self):
        self.color=colorchooser.askcolor(title="Select Color")[-1]
        self.colorDisplay.config(bg=self.color)
    def __bgcSelect(self):
        colo = bg=colorchooser.askcolor(title="Select Color")[-1]
        self.canvas.config(bg=colo)
        self.bgcDisplay.config(bg=colo)
    def __sizeSelect(self,x=4):
        self.size = self.sizeScale.get()
    def __save(self):
        self.canvas.postscript(file="snapshot.eps")
    def __clear(self):
        self.canvas.delete("all")
        self.canvas.config(bg="White")
    def __sizei(self):
        self.sizeScale.set(self.sizeScale.get()+1)
        self.__sizeSelect()
    def __sized(self):
        self.sizeScale.set(self.sizeScale.get()-1)
        self.__sizeSelect()


if __name__ == '__main__':
    p=PaintApp()
    p.Run()