from tkinter import Tk, Label

root = Tk()

cnf={"background":"green", "text":"EXAMPLE TEXT","font": ["Arial", 15],"pady":[5,0]}
lb = Label(root, cnf=cnf).pack()
root.mainloop()
