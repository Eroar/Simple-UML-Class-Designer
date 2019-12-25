from guiClasses import ClassGui
from guiClasses import MembersGui

if __name__ == "__main__":
    from tkinter import Tk
    import json
    root = Tk()
    settingsPath = "D:\\GIT\\Simple-UML-Class-Designer\\newSettings.json"
    with open(settingsPath, "r") as f:
        settings = json.load(f)

    cGui = ClassGui(root, settings)
    cGui.getFrame().grid(row=0, column=0, sticky="snew")
    mGui = MembersGui(root, settings)
    frame = mGui.getFrame()
    frame.grid(row=0, column=1, sticky="snew")
    mGui.insertStuff()
    root.mainloop()