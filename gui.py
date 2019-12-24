from __future__ import annotations
from typing import Any, Dict, List, Set
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import ttk
import json
import os


def donothing():
    pass


class UML_Designer(tkinter.Frame):
    @staticmethod
    def getRoot(settingsPath: str) -> tkinter.Tk:
        ROOT = tkinter.Tk()
        APP = UML_Designer(settingsPath=settingsPath, master=ROOT)
        ROOT.title(APP.getSetting("title"))
        APP.configure(background=APP.getSetting("background"))
        return ROOT

    def __init__(self, settingsPath: str, master: tkinter.Tk = None):
        tkinter.Frame.__init__(self, master)
        self._master = master
        self._settingsPath: str = settingsPath
        self._settings: Dict = self._loadSettings()
        self._openedExtraWindows = []
        self._mainWindow()

    def _loadSettings(self) -> Dict[Any, Any]:
        with open(self._settingsPath, "r") as f:
            return json.load(f)

    def _saveSettings(self) -> None:
        with open(self._settingsPath, "w") as f:
            return json.dump(self._settings, f, indent=4)

    def getSetting(self, settingKey: str) -> Any:
        return self._settings[settingKey]

    def _centerWindow(self, toplevel):
        toplevel.update_idletasks()

        screenWidth = toplevel.winfo_screenwidth()
        screenHeight = toplevel.winfo_screenheight()

        size = tuple(int(q)
                     for q in toplevel.geometry().split('+')[0].split('x'))
        xPad = screenWidth/2 - size[0]/2
        yPad = screenHeight/2 - size[1]/2

        toplevel.geometry("%dx%d+%d+%d" % (size[0], size[1], xPad, yPad))

    def _mainWindow(self):
        # adds a menubar with settings
        menubar: tkinter.Menu = tkinter.Menu(self._master)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open Folder", command=self._onOpenFolder)
        filemenu.add_command(label="Open Last Folder",
                             command=self._openRecentFolder)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self._onExit)
        menubar.add_cascade(label="File", menu=filemenu)

        self._master.config(menu=menubar)
        self._openRecentFolder()

    def _openRecentFolder(self) -> None:
        if ("last-opened-folder" in self._settings) and (self.getSetting("last-opened-folder") != ""):
            self._folderWindow(self.getSetting("last-opened-folder"))
        else:
            tkinter.messagebox.showerror(
                "Error opening a folder", "No previous opened folder found.")

    def _onOpenFolder(self) -> None:
        try:
            folderPath: str = tkinter.filedialog.askdirectory()
            self._settings["last-opened-folder"] = folderPath
            self._saveSettings()
            self._folderWindow(folderPath)
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                "Error opening a folder", "Selected folder was not found")

    def _folderWindow(self, folderPath: str) -> None:
        # allowing the widget to take the full space of the ROOT window
        self.pack(fill="both", expand=1)

        cList: tkinter.Listbox = tkinter.Listbox(self, selectmode=tkinter.SINGLE, background=self.getSetting(
            "class-list-background"), width=self.getSetting("cList-width"), bd=5)
        cList.configure(font=(self.getSetting("cList-font"), self.getSetting(
            "cList-font-size")), background=self.getSetting("cList-background"))
        fileList: List[str] = [f for f in os.listdir(
            folderPath) if os.path.isfile(os.path.join(folderPath, f))]

        for i, file in enumerate(fileList):
            cList.insert(i, file)
        # cList.pack(fill="both")

        addButton: tkinter.Button = tkinter.Button(self, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                   background=self.getSetting("add-button-background"), text="ADD",
                                                   command=lambda: self._addStringToList(cList, self, "Add new class", "Enter new class name:"))

        deleteButton: tkinter.Button = tkinter.Button(self, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                      background=self.getSetting("remove-button-background"), text="DELETE",
                                                      command=lambda: cList.delete(
                                                          cList.curselection())
                                                      if len(cList.curselection()) > 0 else False)

        savingButtonsFrame: tkinter.Frame = tkinter.Frame(
            self, background=self.getSetting("background"))

        saveButton: tkinter.Button = tkinter.Button(savingButtonsFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                    background=self.getSetting("button-background"), text="Save changes",
                                                    command=self._onSaveClassesClick)

        revertButton: tkinter.Button = tkinter.Button(savingButtonsFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                      background=self.getSetting("button-background"), text="revert changes",
                                                      command=self._onSaveClassesClick)

        editorFrame: tkinter.Frame = tkinter.Frame(
            self, background=self.getSetting("background"))

        for x in range(1, 2):
            editorFrame.rowconfigure(x, weight=1)
        for y in range(3):
            editorFrame.columnconfigure(y, weight=1)
            editorFrame.grid_columnconfigure(
                y, minsize=self.getSetting("editorWindow-column-minsize"))

        classDeclarationFrame: tkinter.Frame = tkinter.Frame(
            editorFrame, background=self.getSetting("background"))
        classMembersFrame: tkinter.Frame = tkinter.Frame(
            editorFrame, background="blue")
        classMethodsFrame: tkinter.Frame = tkinter.Frame(
            editorFrame, background="green")

        # CLASS DECLARATION FIELDS
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        tkinter.Label(editorFrame, text="Class", pady=5, font=(self.getSetting("text-font"), self.getSetting(
            "heading-font-size")), background=self.getSetting("background")).grid(row=0, column=0, sticky="wnes")

        # Accesibility
        classAccessibilityVar: tkinter.StringVar = tkinter.StringVar(
            classDeclarationFrame)
        tkinter.Label(classDeclarationFrame, text="Accessibility:", pady=5, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                      background=self.getSetting("background")).grid(row=0, column=0, sticky="ns")
        classAccessibility: tkinter.OptionMenu = tkinter.OptionMenu(
            classDeclarationFrame, classAccessibilityVar, *self.getSetting("accessibility-types"))
        classAccessibility.configure(font=(self.getSetting("text-font"), self.getSetting(
            "text-font-size")), background=self.getSetting("button-background"))
        classAccessibility["menu"].configure(font=(self.getSetting(
            "text-font"), self.getSetting("text-font-size")), background=self.getSetting("button-background"))
        classAccessibility.grid(row=1, column=0, sticky="wnes")

        # Name
        classNameVar: tkinter.StringVar = tkinter.StringVar(
            classDeclarationFrame)
        tkinter.Label(classDeclarationFrame, text="Name:", pady=5, font=(self.getSetting("text-font"), self.getSetting(
            "text-font-size")), background=self.getSetting("background")).grid(row=2, column=0, sticky="wnes")
        className: tkinter.Entry = tkinter.Entry(classDeclarationFrame, textvariable=classNameVar, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                 background=self.getSetting("button-background"), text="", justify="center")
        className.grid(row=3, column=0, sticky="wnes", padx=8)

        # Extends
        classExtendsVar: tkinter.StringVar = tkinter.StringVar(
            classDeclarationFrame)
        tkinter.Label(classDeclarationFrame, text="Extends:", pady=5, font=(self.getSetting(
            "text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=4, column=0, sticky="wnes")
        classExtends: tkinter.Entry = tkinter.Entry(classDeclarationFrame, textvariable=classExtendsVar, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                    background=self.getSetting("button-background"), text="", justify="center")
        classExtends.grid(row=5, column=0, sticky="wnes", padx=8)

        # Empty row
        tkinter.Label(classDeclarationFrame, text="", pady=5, background=self.getSetting(
            "background")).grid(row=6, column=0, sticky="wnes", columnspan=6)

        # Description
        tkinter.Label(classDeclarationFrame, text="Description:", pady=5, font=(self.getSetting("text-font"), self.getSetting(
            "text-font-size")), background=self.getSetting("background")).grid(row=7, column=0, sticky="wnes", columnspan=6)
        classDescription: tkinter.Text = tkinter.Text(classDeclarationFrame, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                      background=self.getSetting("description-background"), width=1)
        classDescription.grid(row=8, column=0, sticky="wnes", columnspan=6)

        classDeclarationFrame.rowconfigure(8, weight=1)
        classDeclarationFrame.columnconfigure(0, weight=1)

        classDeclarationFrame.grid(row=1, column=0, sticky="wens")
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # CLASS Member fields
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        classMembersFrame.grid(row=1, column=1, sticky="wens")

        classMembersFrame.rowconfigure(1, weight=1)
        classMembersFrame.columnconfigure(0, weight=1)
        classMembersFrame.columnconfigure(1, weight=1)
        

        tkinter.Label(editorFrame, text="Members", pady=5, font=(self.getSetting("text-font"), self.getSetting(
            "heading-font-size")), background=self.getSetting("background")).grid(row=0, column=1, sticky="wnes")

        membersList: tkinter.Listbox = tkinter.Listbox(
            classMembersFrame, selectmode=tkinter.SINGLE, background=self.getSetting("button-background"))
        membersList.configure(justify="center", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")))
        for i in range(20):
            membersList.insert(i, "+ Member_" + str(i) + " : string")
        membersList.grid(row=1, columnspan=2, sticky="wens")
        membersList.bind("<Double-Button-1>", lambda event: self._onMembersListClick(
            self, membersList.curselection(), membersList))

        addMemberButton: tkinter.Button = tkinter.Button(classMembersFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                   background=self.getSetting("add-button-background"), text="Add member",
                                                   command=lambda: self._addStringToList(membersList, self, "Add new member", "Enter new member's name:"))
        addMemberButton.grid(row=0, column=0, sticky="wens")

        deleteMemberButton: tkinter.Button = tkinter.Button(classMembersFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                      background=self.getSetting("remove-button-background"), text="Remove member",
                                                      command=lambda: membersList.delete(
                                                          membersList.curselection())
                                                      if len(membersList.curselection()) > 0 else False)
        deleteMemberButton.grid(row=0, column=1, sticky="wens")
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # CLASS Methods
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        classMethodsFrame.grid(row=1, column=2, sticky="wens")

        classMethodsFrame.rowconfigure(1, weight=1)
        classMethodsFrame.columnconfigure(0, weight=1)
        classMethodsFrame.columnconfigure(1, weight=1)

        tkinter.Label(editorFrame, text="Methods", pady=5, font=(self.getSetting("text-font"), self.getSetting(
            "heading-font-size")), background=self.getSetting("background")).grid(row=0, column=2, sticky="wnes")

        methodsList: tkinter.Listbox = tkinter.Listbox(
            classMethodsFrame, selectmode=tkinter.SINGLE, background=self.getSetting("button-background"))
        methodsList.configure(justify="center", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")))
        for i in range(20):
            methodsList.insert(i, "+ Method_" + str(i) + " : string")
        methodsList.grid(row=1, column=0, columnspan=2, sticky="wens")
        methodsList.bind("<Double-Button-1>", lambda event: self._onMethodsListClick(
            classMethodsFrame, methodsList.curselection(), methodsList))

        addMethodButton: tkinter.Button = tkinter.Button(classMethodsFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                   background=self.getSetting("add-button-background"), text="Add method",
                                                   command=lambda: self._addStringToList(methodsList, self, "Add new method", "Enter new method's name:"))
        addMethodButton.grid(row=0, column=0, sticky="wens")

        deleteMethodButton: tkinter.Button = tkinter.Button(classMethodsFrame, font=(self.getSetting("button-font"), self.getSetting("button-font-size")),
                                                      background=self.getSetting("remove-button-background"), text="Remove method",
                                                      command=lambda: methodsList.delete(
                                                          methodsList.curselection())
                                                      if len(methodsList.curselection()) > 0 else False)
        deleteMethodButton.grid(row=0, column=1, sticky="wens")
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        addButton.grid(row=0, column=0, sticky="wens", padx=5, pady=5)
        deleteButton.grid(row=0, column=1, sticky="wens", padx=5, pady=5)
        cList.grid(row=1, column=0, columnspan=2, sticky="wens")
        savingButtonsFrame.grid(row=2, column=2, sticky="wens")
        editorFrame.grid(row=0, column=2, rowspan=2, sticky="wens")

        revertButton.pack(side="right")
        saveButton.pack(side="right")

        cList.bind("<Double-Button-1>",
                   lambda event: self._oncListClick(cList.curselection(), editorFrame))

    def _addStringToList(self, classList: tkinter.Listbox, parent: tkinter.Frame, title: str, labelText: str) -> None:
        add2ListWindow: tkinter.Toplevel = tkinter.Toplevel(parent)
        add2ListWindow.transient([parent])
        add2ListWindow.wm_title(title)
        add2ListWindow.resizable(False, False)
        add2ListWindow.configure(background=self.getSetting("background"))

        tkinter.Label(add2ListWindow, text=labelText, font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).pack(side="top", padx=10, pady=(7, 2))

        classNameEntry: tkinter.Entry = tkinter.Entry(
            add2ListWindow, background=self.getSetting("button-background"), justify="center", width=25)
        classNameEntry.pack(side="top", pady=10, padx=20, fill="x")

        saveNewClass: tkinter.Button = tkinter.Button(add2ListWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Add",
            command=lambda: [classList.insert(tkinter.END, classNameEntry.get()), add2ListWindow.destroy()] if len(classNameEntry.get()) > 0 else None)
        saveNewClass.pack(side="top")

        self._centerWindow(add2ListWindow)

    def _onSaveClassesClick(self) -> None:
        pass

    def _onRevertChangesClick(self) -> None:
        pass

    def _onMembersListClick(self, parent: tkinter.Frame, index: List[int], membersList: tkinter.Listbox) -> None:
        memberWindow: tkinter.Toplevel = tkinter.Toplevel(parent)
        memberWindow.transient([parent])
        memberWindow.wm_title("Member details")
        memberWindow.configure(background=self.getSetting("background"))

        memberWindow.rowconfigure(7, weight=1)
        for y in range(2):
            memberWindow.columnconfigure(y, weight=1)

        # Name
        tkinter.Label(memberWindow, text="Name:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=0, column=0, columnspan=2)

        memberNameEntry: tkinter.Entry = tkinter.Entry(
            memberWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        memberNameEntry.grid(row=1, column=0, columnspan=2,
                             sticky="wnes", padx=10, pady=5)

        # Accessibility
        tkinter.Label(memberWindow, text="Accessibility:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=2, column=0, columnspan=2)

        memberAccessibilityVar: tkinter.StringVar = tkinter.StringVar(
            memberWindow)
        memberAccessibility: tkinter.OptionMenu = tkinter.OptionMenu(
            memberWindow, memberAccessibilityVar, *self.getSetting("accessibility-types"))
        memberAccessibility.configure(font=(self.getSetting("text-font"), self.getSetting(
            "text-font-size")), background=self.getSetting("button-background"))
        memberAccessibility["menu"].configure(font=(self.getSetting(
            "text-font"), self.getSetting("text-font-size")), background=self.getSetting("button-background"))
        memberAccessibility.grid(
            row=3, column=0, columnspan=2, sticky="ns", pady=5)

        # Type
        tkinter.Label(memberWindow, text="Type:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=4, column=0, columnspan=2)

        memberTypeEntry: tkinter.Entry = tkinter.Entry(
            memberWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        memberTypeEntry.grid(row=5, column=0, columnspan=2,
                             sticky="wnes", padx=10, pady=5)

        # Description
        tkinter.Label(memberWindow, text="Description:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=6, column=0, columnspan=2)
        memberDescription: tkinter.Text = tkinter.Text(memberWindow, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                       background=self.getSetting("description-background"), width=self.getSetting("description-width"), height=self.getSetting("description-height"))
        memberDescription.grid(row=7, column=0, columnspan=2,
                               sticky="wnes", padx=10, pady=10)

        # Save button
        saveMember: tkinter.Button = tkinter.Button(memberWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Add",
            command=lambda: None)  # ToDO
        saveMember.grid(row=8, column=0, sticky="wnes", padx=10, pady=5)

        # Cancel button
        cancelChanges: tkinter.Button = tkinter.Button(memberWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Cancel",
            command=lambda: memberWindow.destroy())
        cancelChanges.grid(row=8, column=1, sticky="wnes", padx=10, pady=5)

        self._centerWindow(memberWindow)

    def _onMethodsListClick(self, parent: tkinter.Frame, index: List[int], methodsList: tkinter.Listbox) -> None:
        methodWindow: tkinter.Toplevel = tkinter.Toplevel(parent)
        methodWindow.transient([parent])
        methodWindow.wm_title("Method details")
        methodWindow.configure(background=self.getSetting("background"))

        # arguments
        methodWindow.rowconfigure(7, weight=1)
        # description
        methodWindow.rowconfigure(9, weight=1)
        for y in range(2):
            methodWindow.columnconfigure(y, weight=1)

        # Name
        tkinter.Label(methodWindow, text="Name:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=0, column=0, columnspan=2)

        methodNameEntry: tkinter.Entry = tkinter.Entry(
            methodWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        methodNameEntry.grid(row=1, column=0, columnspan=2,
                             sticky="wnes", padx=10, pady=5)

        # Accessibility
        tkinter.Label(methodWindow, text="Accessibility:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=2, column=0, columnspan=2)

        methodAccessibilityVar: tkinter.StringVar = tkinter.StringVar(
            methodWindow)
        methodAccessibility: tkinter.OptionMenu = tkinter.OptionMenu(
            methodWindow, methodAccessibilityVar, *self.getSetting("accessibility-types"))
        methodAccessibility.configure(font=(self.getSetting("text-font"), self.getSetting(
            "text-font-size")), background=self.getSetting("button-background"))
        methodAccessibility["menu"].configure(font=(self.getSetting(
            "text-font"), self.getSetting("text-font-size")), background=self.getSetting("button-background"))
        methodAccessibility.grid(
            row=3, column=0, columnspan=2, sticky="ns", pady=5)

        # Output Type
        tkinter.Label(methodWindow, text="Output type:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=4, column=0, columnspan=2)

        methodOutputTypeEntry: tkinter.Entry = tkinter.Entry(
            methodWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        methodOutputTypeEntry.grid(
            row=5, column=0, columnspan=2, sticky="wnes", padx=10, pady=5)

        # Input arguments
        tkinter.Label(methodWindow, text="Input arguments:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=6, column=0, columnspan=2)

        inputArgsList: tkinter.Listbox = tkinter.Listbox(
            methodWindow, selectmode=tkinter.SINGLE, background=self.getSetting("list-background"), width=25, bd=5)
        inputArgsList.bind("<Double-Button-1>", lambda event: self._onArgsListClick(
            methodWindow, inputArgsList.curselection(), inputArgsList))
        inputArgsList.grid(row=7, column=0, columnspan=2,
                           sticky="wnes", padx=10, pady=5)

        # ToDo
        for i in range(5):
            inputArgsList.insert(i, "+ " + f"argument_{i}: string")
        argsLen = len(inputArgsList.get(0, tkinter.END))
        inputArgsList.configure(height=argsLen, font=(self.getSetting("list-font"), self.getSetting(
            "list-font-size")), background=self.getSetting("list-background"), justify="center")

        # Description
        tkinter.Label(methodWindow, text="Description:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=8, column=0, columnspan=2)
        memberDescription: tkinter.Text = tkinter.Text(methodWindow, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                       background=self.getSetting("description-background"), width=self.getSetting("description-width"), height=self.getSetting("description-height"))
        memberDescription.grid(row=9, column=0, columnspan=2,
                               sticky="wnes", padx=10, pady=10)

        # Save button
        saveMember: tkinter.Button = tkinter.Button(methodWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Add",
            command=lambda: None)  # ToDO
        saveMember.grid(row=10, column=0, sticky="wnes", padx=10, pady=5)

        # Cancel button
        cancelChanges: tkinter.Button = tkinter.Button(methodWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Cancel",
            command=lambda: methodWindow.destroy())
        cancelChanges.grid(row=10, column=1, sticky="wnes", padx=10, pady=5)

        self._centerWindow(methodWindow)

    def _onArgsListClick(self, parent: tkinter.Toplevel, index: List[int], argsList: tkinter.Listbox) -> None:
        argWindow: tkinter.Toplevel = tkinter.Toplevel(parent)
        argWindow.transient([parent])
        argWindow.wm_title("Argument details")
        argWindow.configure(background=self.getSetting("background"))

        argWindow.rowconfigure(5, weight=1)
        for y in range(2):
            argWindow.columnconfigure(y, weight=1)

        # Name
        tkinter.Label(argWindow, text="Name:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=0, column=0, columnspan=2)

        memberNameEntry: tkinter.Entry = tkinter.Entry(
            argWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        memberNameEntry.grid(row=1, column=0, columnspan=2,
                             sticky="wnes", padx=10, pady=5)

        # Type
        tkinter.Label(argWindow, text="Type:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=2, column=0, columnspan=2)

        memberTypeEntry: tkinter.Entry = tkinter.Entry(
            argWindow, background=self.getSetting("button-background"), justify="center", font=(self.getSetting("text-font"), self.getSetting("text-font-size")))
        memberTypeEntry.grid(row=3, column=0, columnspan=2,
                             sticky="wnes", padx=10, pady=5)

        # Description
        tkinter.Label(argWindow, text="Description:", font=(
            self.getSetting("text-font"), self.getSetting("text-font-size")), background=self.getSetting("background")).grid(row=4, column=0, columnspan=2)
        memberDescription: tkinter.Text = tkinter.Text(argWindow, font=(self.getSetting("text-font"), self.getSetting("text-font-size")),
                                                       background=self.getSetting("description-background"), width=self.getSetting("description-width"), height=self.getSetting("description-height"))
        memberDescription.grid(row=5, column=0, columnspan=2,
                               sticky="wnes", padx=10, pady=10)

        # Save button
        saveMember: tkinter.Button = tkinter.Button(argWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Add",
            command=lambda: None)  # ToDO
        saveMember.grid(row=6, column=0, sticky="wnes", padx=10, pady=5)

        # Cancel button
        cancelChanges: tkinter.Button = tkinter.Button(argWindow, font=(
            self.getSetting("button-font"), self.getSetting("button-font-size")), background=self.getSetting("background"), text="Cancel",
            command=lambda: argWindow.destroy())
        cancelChanges.grid(row=6, column=1, sticky="wnes", padx=10, pady=5)

        self._centerWindow(argWindow)

    def _oncListClick(self, index: List[int], editorFrame: tkinter.Frame) -> None:
        print("index:", index[0])
        self._updateEditorFrame(index[0], editorFrame)

    def _updateEditorFrame(self, index: int, editorFrame: tkinter.Frame) -> None:
        pass

    def _onExit(self) -> None:
        self._master.quit()
