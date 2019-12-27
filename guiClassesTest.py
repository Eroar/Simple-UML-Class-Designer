from simpleUmlDesigner.guiClasses import ClassEditor
from simpleUmlDesigner.dataClasses import *
import json
from tkinter import Tk

if __name__ == "__main__":
    settingsPath = "D:\\Coding\\GIT\Simple-UML-Class-Designer\\newSettings.json"
    with open(settingsPath, "r") as f:
        settings = json.load(f)

    cInfo = ClassInfo("NAME", "ACCESS", "EXTEND", "DESCRIPT")
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    classEditor = ClassEditor(root, settings)
    classEditor.grid(row=0, column=0, sticky="snew")
    classEditor._classFrame.setClassInfo(cInfo)
    root.mainloop()
