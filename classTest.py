from guiClasses import ClassGui

if __name__ == "__main__":
    from tkinter import Tk
    import json
    root = Tk()
    settingsPath = "D:\\Coding\GIT\\Simple-UML-Class-Designer\\settings.json"
    with open(settingsPath, "r") as f:
        settings = json.load(f)

    cGui = ClassGui(settings)
    cGui.getFrame(root).pack(fill="both")
    root.mainloop()