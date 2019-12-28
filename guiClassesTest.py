from simpleUmlDesigner.guiClasses import ClassEditor, MemberFrame
from simpleUmlDesigner.dataClasses import *
import json
from tkinter import Tk

def foo():
    print("foo function")

if __name__ == "__main__":
    settingsPath = "D:\\Coding\\GIT\Simple-UML-Class-Designer\\simpleUmlDesigner\\newSettings.json"
    with open(settingsPath, "r") as f:
        settings = json.load(f)

    newDiag = Diagram("New test Diag")

    newMember = Member(name="MemberTest", type="int", accessibility="public")
    newDiag.addMember(newMember)    

    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    classEditor = ClassEditor(root, settings)
    classEditor.grid(row=0, column=0, sticky="snew")
    classEditor.editDiag(newDiag)
    root.mainloop()
    # classEditor._classFrame.setClassInfo(cInfo)
