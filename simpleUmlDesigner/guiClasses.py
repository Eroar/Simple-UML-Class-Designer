from __future__ import annotations

import copy
import json
from tkinter import (BROWSE, END, Button, Entry, Frame, Label, Listbox,
                     OptionMenu, StringVar, Text, Tk, Toplevel)
from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union, cast

from .dataClasses import ClassInfo, Diagram, EditingManager, Member, Method, Input

_parentType = Union[Frame, Toplevel, Tk]


class ClassContentFrame(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        super().__init__(
            parent, background=self._settings["cnfs"]["general"]["background"])
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}
        self._parent = parent

    def _setFramesSequence(self, newSequence: List[str]) -> None:
        self._frameElementsSequence = newSequence

    def _lateInit(self) -> None:
        # places all elements on frame
        self._placeWidgets()

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getCnf(self, *cnfNames: str) -> Dict[str, Any]:
        newCnf: Dict[str, Any] = {}
        for cnf in cnfNames:
            newCnf = {**newCnf, **self._settings["cnfs"][cnf]}
        return newCnf

    def _getLabel(self, text: str) -> Label:
        cnf = self._getCnf("general", "Label")
        cnf["text"] = text
        label: Label = Label(self, cnf)
        return label

    def _getEntry(self) -> Tuple[Entry, StringVar]:
        cnf = self._getCnf("general", "field", "justify-center")
        textVar: StringVar = StringVar(self)
        entry: Entry = Entry(self, cnf, textvariable=textVar)
        return entry, textVar

    def _getText(self) -> Text:
        cnf = self._getCnf("general", "Text", "field")
        text: Text = Text(self, cnf)
        return text

    def _getListBox(self) -> Listbox:
        cnf = self._getCnf("general", "Listbox", "justify-center")
        listbox: Listbox = Listbox(self, cnf)
        return listbox

    def _getOptionMenu(self) -> Tuple[OptionMenu, StringVar]:
        cnf = self._getCnf("general", "field")
        optionMenunVar: StringVar = StringVar(self)
        optionMenu: OptionMenu = OptionMenu(
            self, optionMenunVar, *self._settings["cnfs"]["OptionMenu-values"])

        optionMenu.configure(cnf)

        optionMenu["menu"].configure(cnf)

        return optionMenu, optionMenunVar

    def _getButton(self) -> Button:
        cnf = self._getCnf("general", "field")
        button: Button = Button(self, cnf)
        return button

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        self._frameElements = {}
        elementsNotFound: List[str] = []
        for key in self._frameElementsSequence:
            keySplitted = key.split("_")
            name: str = keySplitted[0]
            widget: str = keySplitted[-1]

            if widget == "Label":
                if name == "Empty":
                    # Name_Empty_Label
                    self._frameElements[key] = self._getLabel("")
                else:
                    self._frameElements[key] = self._getLabel(name)
            elif widget == "Entry":
                self._frameElements[key], self._frameElements[key +
                                                              "Var"] = self._getEntry()
            elif widget == "Text":
                self._frameElements[key] = self._getText()
            elif widget == "Listbox":
                self._frameElements[key] = self._getListBox()
            elif widget == "OptionMenu":
                self._frameElements[key], self._frameElements[key +
                                                              "Var"] = self._getOptionMenu()
            else:
                elementsNotFound.append(key)
        elementsFound: List[str] = [
            element for element in self._frameElementsSequence if element not in elementsNotFound]
        return elementsFound, elementsNotFound

    def _placeWidgets(self) -> None:
        elementsFound = self._updateFrameElements()[0]
        for element in elementsFound:
            self._frameElements[element].pack(side="top")


class ClassEditor(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(
            parent, background=settings["cnfs"]["general"]["background"])
        self._classInfoFrame = ClassInfoFrame(self, settings)
        self._membersFrame = MembersFrame(self, settings)
        self._methodsFrame = MethodsFrame(self, settings)

        self._editingManager = EditingManager()

        self._placeElements()

    def _placeElements(self):
        self.rowconfigure(0, weight=1)
        for y in range(3):
            self.columnconfigure(y, weight=1)
        self._classInfoFrame.grid(row=0, column=0, sticky="snew")
        self._membersFrame.grid(row=0, column=1, sticky="snew")
        self._methodsFrame.grid(row=0, column=2, sticky="snew")

    def editDiag(self, diag2Edit: Diagram) -> None:
        self._editingManager.setNewOriginalDiag(diag2Edit)
        diag2Edit = self._editingManager.getDiag2Edit()
        self._classInfoFrame.setClassInfo(diag2Edit.getClassInfo())

        self._membersFrame.setMembers(diag2Edit.getMembers())


class ClassInfoFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        super()._setFramesSequence([
            "Name:_Label",
            "Name_Entry",
            "Accessibility:_Label",
            "Accesibility_OptionMenu",
            "Extends:_Label",
            "Extends_Entry",
            "Empty_Label",
            "Description:_Label",
            "Description_Text"
        ])
        super()._lateInit()
        self._classInfo: ClassInfo

    def _getElementsDict(self) -> Dict["str", Any]:
        """A function that is used purely to shorten syntax"""
        d = {}
        d["name"] = self._frameElements["Name_EntryVar"]
        d["accessibility"] = self._frameElements["Accesibility_OptionMenuVar"]
        d["extends"] = self._frameElements["Extends_EntryVar"]
        d["description"] = self._frameElements["Description_Text"]
        return d

    def setClassInfo(self, newClassInfo: ClassInfo):
        self._classInfo = newClassInfo
        elements = self._getElementsDict()
        elements["name"].set(newClassInfo.getName())
        elements["accessibility"].set(newClassInfo.getAccessibility())
        elements["extends"].set(newClassInfo.getExtends())
        elements["description"].delete(1.0, END)
        elements["description"].insert(END, newClassInfo.getDescription())

    def getClassInfo(self):
        elements = self._getElementsDict()
        self._classInfo.setName(elements["name"].get())
        self._classInfo.setAccessibility(elements["accessibility"].get())
        self._classInfo.setExtends(elements["extends"].get())
        self._classInfo.setDescription(elements["description"].get(1.0, END))

    def _placeWidgets(self) -> None:
        elementsFound = super()._updateFrameElements()[0]
        for element in elementsFound:
            if element == "Accesibility_OptionMenu":
                self._frameElements[element].pack(
                    side="top", fill="y", padx=10, pady=(0, 0))

            elif element[-5:] == "Label":
                self._frameElements[element].pack(
                    side="top", fill="y", padx=10, pady=(5, 2))
            else:
                self._frameElements[element].pack(
                    side="top", fill="both", padx=10, pady=2)


class EnhListbox(Listbox):
    def __init__(self, master: _parentType, cnf: Dict[str, Any], onDoubleClick: Callable[[int], Any]):
        super().__init__(master, cnf)
        self._onDoubleClick: Callable[[int], Any] = onDoubleClick
        self._elementDragged: bool = False
        self._lastDraggingIndex: int = -1
        self._dragging: bool = False

        self.bind("<Double-Button-1>",
                  lambda event: self._onDoubleClickInternal())
        self._pickedElement: str = ""
        self.bind("<Button-3>",
                  lambda event: self._onRightClick(event))
        self.bind("<B3-Motion>",
                  lambda event: self._onDragging(event))
        self.bind("<ButtonRelease-3>",
                  lambda event: self._onRightRelease(event))

    def _getNearestIndex(self, y) -> int:
        index = self.nearest(y)
        if index == -1:
            index = 0
        return index

    def _onRightClick(self, event) -> None:
        index = self.nearest(event.y)
        if index != -1:
            self._dragging = True
            self.selection_clear(0, END)
            self.selection_set(index, index)
            self._pickedElement = copy.copy(self.get(index, index)[0])
            self._lastDraggingIndex = index

    def _onRightRelease(self, event) -> None:
        self._dragging = False

    def _onDragging(self, event) -> None:
        if self._dragging:
            index = self._getNearestIndex(event.y)
            if index != self._lastDraggingIndex:
                if self._lastDraggingIndex != -1:
                    self.delete(self._lastDraggingIndex,
                                self._lastDraggingIndex)
                index = self._getNearestIndex(event.y)

                if self.size() > 0:
                    if event.y > self.bbox(END)[1]+15:
                        index += 1
                self.insert(index, self._pickedElement)
                self.selection_clear(0, END)
                self.selection_set(index, index)
                self._lastDraggingIndex = index

    def _onDoubleClickInternal(self) -> None:
        try:
            index = self.curselection()[0]
        except IndexError:
            return
        self._onDoubleClick(index)


class MemberFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any], onOkButton: Callable):
        super().__init__(parent, settings)
        super()._setFramesSequence([
            "Name:_Label",
            "Name_Entry",
            "Accessibility:_Label",
            "Accesibility_OptionMenu",
            "Type_Label",
            "Type_Entry",
            "Default value:_Label",
            "DefaultValue_Entry",
            "Description:_Label",
            "Description_Text",
            "ok_OkButton",
            "cancel_CancelButton"
        ])
        self._member: Member
        self._onOkButtonOutFunc = onOkButton
        super()._lateInit()

    def _getOkButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._onOkButton, text="ok")
        return button

    def _onOkButton(self) -> None:
        self.getMember()
        self._onOkButtonOutFunc()
        self._parent.destroy()

    def _getCancelButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._parent.destroy, text="cancel")
        return button

    def _getElementsDict(self) -> Dict["str", Any]:
        """A function that is used purely to shorten syntax"""
        d = {}
        d["name"] = self._frameElements["Name_EntryVar"]
        d["accessibility"] = self._frameElements["Accesibility_OptionMenuVar"]
        d["type"] = self._frameElements["Type_EntryVar"]
        d["defaultValue"] = self._frameElements["DefaultValue_EntryVar"]
        d["description"] = self._frameElements["Description_Text"]
        return d

    def setMember(self, member: Member):
        self._member = member
        elements = self._getElementsDict()
        elements["name"].set(self._member.getName())
        elements["accessibility"].set(self._member.getAccessibility())
        elements["type"].set(self._member.getType())
        elements["defaultValue"].set(self._member.getDefaulValue())
        elements["description"].delete(1.0, END)
        elements["description"].insert(END, self._member.getDescription())

    def getMember(self):
        elements = self._getElementsDict()
        self._member.setName(elements["name"].get())
        self._member.setAccessibility(elements["accessibility"].get())
        self._member.setType(elements["type"].get())
        self._member.setDefaulValue(elements["defaultValue"].get())
        self._member.setDescription(elements["description"].get(1.0, END))

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        newElementsNotFound: List[str] = []
        for key in elementsNotFound:

            if key == "ok_OkButton":
                self._frameElements[key] = self._getOkButton()
                elementsFound.append(key)
            elif key == "cancel_CancelButton":
                self._frameElements[key] = self._getCancelButton()
            else:
                newElementsNotFound.append(key)

        for element in elementsNotFound:
            if element not in newElementsNotFound:
                elementsFound.append(element)

        return elementsFound, newElementsNotFound

    def _placeWidgets(self):
        self.rowconfigure(1, weight=1)
        for y in range(2):
            self.columnconfigure(y, weight=1)
        elementsFound, elementsNotFound = self._updateFrameElements()

        row = 0
        for key in elementsFound:
            if key == "ok_OkButton":
                self._frameElements[key].grid(
                    row=row, column=0, sticky="nesw", padx=5)
            elif key == "cancel_CancelButton":
                self._frameElements[key].grid(
                    row=row, column=1, sticky="nesw", padx=5)
            else:
                self._frameElements[key].grid(
                    row=row, column=0, sticky="nesw", columnspan=2, padx=10)
                row += 1


class MembersFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._setFramesSequence([
            "addMember_AddButton",
            "removeMember_RemoveButton",
            "members_MembersListbox"
        ])
        super()._lateInit()
        self._membersListGui: EnhListbox = self._frameElements["members_MembersListbox"]

        self._members: List[Member]

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("AddButton")
        cnf["command"] = self._onAddButton
        button.configure(cnf)
        return button

    def _getElementsDict(self) -> Dict["str", Any]:
        """A function that is used purely to shorten syntax"""
        d = {}
        d["membersListbox"] = self._frameElements["members_MembersListbox"]
        return d

    def setMembers(self, membersList: List[Member]) -> None:
        d = self._getElementsDict()
        membersListbox = d["membersListbox"]
        membersListbox.delete(0, END)
        self._members = membersList
        strList: List[str] = [memberStr.getStr()
                              for memberStr in self._members]

        for memberStr in strList:
            membersListbox.insert(END, memberStr)

    def getMembers(self) -> None:
        d = self._getElementsDict()
        membersStrs = d["membersListbox"].get(0, END)

        for strIndex, memberStr in enumerate(membersStrs):
            for memberIndex, member in enumerate(self._members):
                if member.getStr() == memberStr:
                    if strIndex != memberIndex:
                        tmp: Member = self._members[strIndex]
                        self._members[strIndex] = self._members[memberIndex]
                        self._members[memberIndex] = tmp
                        break

    def _onAddButton(self) -> None:
        index: Union[str, int]
        try:
            index = self._membersListGui.curselection()[0] + 1
        except IndexError:
            index = END
        newMember: Member = Member()
        memberWindow: Toplevel = Toplevel(self)
        memberFrame: MemberFrame = MemberFrame(
            memberWindow, self._settings, onOkButton=lambda: self._onOkButton(newMember, index))
        memberFrame.setMember(newMember)
        memberWindow.title = "Member"
        memberFrame.pack(fill="both")


    def _onOkButton(self, newMember: Member, index: Union[int, str]):
        if index == "end":
            self._members.append(newMember)
        else:
            self._members.insert(cast(int, index), newMember)
        self._membersListGui.insert(index, newMember.getStr())

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("RemoveButton")
        cnf["command"] = self._onRemoveButton
        button.configure(cnf)
        return button

    def _onRemoveButton(self) -> None:
        try:
            index: int = self._membersListGui.curselection()[0]
            self.getMembers()
            del self._members[index]
            self._membersListGui.delete(index)
        except IndexError:
            pass

    def _getMembersListbox(self) -> EnhListbox:
        cnf: Dict[str, Any] = super()._getCnf(
            "general", "field", "justify-center")
        membersListbox: EnhListbox = EnhListbox(
            self, cnf, self._onMembersListboxDoubleClick)
        return membersListbox

    def _onMembersListboxDoubleClick(self, index: int) -> None:
        print(f"Double click {index}")

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        newElementsNotFound: List[str] = []
        for key in elementsNotFound:

            if key == "addMember_AddButton":
                self._frameElements[key] = self._getAddButton()
                elementsFound.append(key)
            elif key == "removeMember_RemoveButton":
                self._frameElements[key] = self._getRemoveButton()
            elif key == "members_MembersListbox":
                self._frameElements[key] = self._getMembersListbox()
            else:
                newElementsNotFound.append(key)

        for element in elementsNotFound:
            if element not in newElementsNotFound:
                elementsFound.append(element)

        return elementsFound, newElementsNotFound

    def _placeWidgets(self) -> None:
        self.rowconfigure(1, weight=1)
        for y in range(2):
            self.columnconfigure(y, weight=1)
        elementsFound, elementsNotFound = self._updateFrameElements()

        for key in elementsFound:
            if key == "addMember_AddButton":
                self._frameElements[key].grid(
                    row=0, column=0, sticky="nesw")
            elif key == "removeMember_RemoveButton":
                self._frameElements[key].grid(
                    row=0, column=1, sticky="nesw")
            elif key == "members_MembersListbox":
                self._frameElements[key].grid(
                    row=1, column=0, sticky="nesw", columnspan=2)


class InputFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        super()._setFramesSequence([
            "Name:_Label",
            "Name_Entry",
            "Type_Label",
            "Type_Entry",
            "Default value:_Label",
            "DefaultValue_Entry",
            "Description:_Label",
            "Description_Text"
        ])
        super()._lateInit()
        self._input: Input

    def _getElementsDict(self) -> Dict["str", Any]:
        """A function that is used purely to shorten syntax"""
        d = {}
        d["name"] = self._frameElements["Name_EntryVar"]
        d["type"] = self._frameElements["Type_EntryVar"]
        d["defaultValue"] = self._frameElements["DefaultValue_EntryVar"]
        d["description"] = self._frameElements["Description_Text"]
        return d

    def setInput(self, inputClass: Input):
        self._input = inputClass
        elements = self._getElementsDict()
        elements["name"].set(self._input.getName())
        elements["type"].set(self._input.getType())
        elements["defaultValue"].set(self._input.getDefaulValue())
        elements["description"].delete(1.0, END)
        elements["description"].insert(END, self._input.getDescription())

    def getInput(self):
        elements = self._getElementsDict()
        self._input.setName(elements["name"].get())
        self._input.setType(elements["type"].get())
        self._input.setDefaulValue(elements["defaultValue"].get())
        self._input.setDescription(elements["description"].get(1.0, END))


class MethodsFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._setFramesSequence([
            "addMethod_AddButton",
            "removeMethod_RemoveButton",
            "methods_MethodsListbox"
        ])
        super()._lateInit()
        self._methodsList: EnhListbox = self._frameElements["methods_MethodsListbox"]

        # Testing
        self.i = 0

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("AddButton")
        cnf["command"] = self._onAddButton
        button.configure(cnf)
        return button

    def _onAddButton(self) -> None:
        index: Union[str, int]
        try:
            index = self._methodsList.curselection()[0] + 1
        except IndexError:
            index = END
        self._methodsList.insert(index, f"VALUE {self.i}")
        self.i += 1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("RemoveButton")
        cnf["command"] = self._onRemoveButton
        button.configure(cnf)
        return button

    def _onRemoveButton(self) -> None:
        try:
            index: int = self._methodsList.curselection()[0]
            self._methodsList.delete(index)
        except IndexError:
            pass

    def _getMethodsListbox(self) -> EnhListbox:
        cnf: Dict[str, Any] = super()._getCnf(
            "general", "field", "justify-center")
        methodsListbox: EnhListbox = EnhListbox(
            self, cnf, self._onMethodsListboxDoubleClick)
        return methodsListbox

    def _onMethodsListboxDoubleClick(self, index: int) -> None:
        print(f"Double click {index}")

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        newElementsNotFound: List[str] = []
        for key in elementsNotFound:

            if key == "addMethod_AddButton":
                self._frameElements[key] = self._getAddButton()
                elementsFound.append(key)
            elif key == "removeMethod_RemoveButton":
                self._frameElements[key] = self._getRemoveButton()
            elif key == "methods_MethodsListbox":
                self._frameElements[key] = self._getMethodsListbox()
            else:
                newElementsNotFound.append(key)

        for element in elementsNotFound:
            if element not in newElementsNotFound:
                elementsFound.append(element)

        return elementsFound, newElementsNotFound

    def _placeWidgets(self) -> None:
        self.rowconfigure(1, weight=1)
        for y in range(2):
            self.columnconfigure(y, weight=1)
        elementsFound, elementsNotFound = self._updateFrameElements()

        for key in elementsFound:
            if key == "addMethod_AddButton":
                self._frameElements[key].grid(
                    row=0, column=0, sticky="nesw")
            elif key == "removeMethod_RemoveButton":
                self._frameElements[key].grid(
                    row=0, column=1, sticky="nesw")
            elif key == "methods_MethodsListbox":
                self._frameElements[key].grid(
                    row=1, column=0, sticky="nesw", columnspan=2)


class UML_Designer(Frame):
    @staticmethod
    def getRoot(settingsPath: str) -> tkinter.Tk:
        ROOT = Tk()
        APP = UML_Designer(settingsPath=settingsPath, master=ROOT)
        ROOT.title(APP.getSetting("title"))
        APP.configure(background=APP.getSetting("background"))
        return ROOT

    def __init__(self, settingsPath: str, master: tkinter.Tk):
        tkinter.Frame.__init__(self, master)
        self._master: tkinter.Tk = master
        self._settingsPath: str = settingsPath
        self._settings: Dict = self._loadSettings()
        self._openedExtraWindows = []
        self._mainWindow()

    def getSetting(self, settingKey: str) -> Any:
        return self._settings["program-settings"][settingKey]

    def _saveSettings(self) -> None:
        with open(self._settingsPath, "w") as f:
            return json.dump(self._settings, f, indent=4)

    def _centerWindow(self, toplevel):
        toplevel.update_idletasks()

        screenWidth = toplevel.winfo_screenwidth()
        screenHeight = toplevel.winfo_screenheight()

        size = tuple(int(q)
                     for q in toplevel.geometry().split('+')[0].split('x'))
        xPad = screenWidth/2 - size[0]/2
        yPad = screenHeight/2 - size[1]/2

        toplevel.geometry("%dx%d+%d+%d" % (size[0], size[1], xPad, yPad))
