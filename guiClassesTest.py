from guiClasses import ClassFrame
from guiClasses import MembersFrame

if __name__ == "__main__":
    from tkinter import Tk
    import json
    root = Tk()
    root.rowconfigure(0, weight=1)
    for y in range(2):
        root.columnconfigure(y,weight=1)
    settingsPath = "D:\\Coding\\GIT\Simple-UML-Class-Designer\\newSettings.json"
    with open(settingsPath, "r") as f:
        settings = json.load(f)

    cGui = ClassFrame(root, settings).grid(row=0, column=0, sticky="snew")
    mGui = MembersFrame(root, settings)
    mGui.grid(row=0, column=1, sticky="snew")
    root.mainloop()