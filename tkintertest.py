import tkinter

def getButtonFrame(parent):
	frame = tkinter.Frame(parent, background="red")
	btn = tkinter.Button(frame, text="Button1")
	btn.pack()
	return frame

rt=tkinter.Tk()

mainFrame = tkinter.Frame(rt, background="green")
entry = tkinter.Entry(mainFrame, background="yellow", width=20)
entry.pack()
getButtonFrame(rt).grid(row=0,column=1)
mainFrame.grid(row=0,column=0)
rt.mainloop()