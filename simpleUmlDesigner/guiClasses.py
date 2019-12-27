from __future__ import annotations

from tkinter import (BROWSE, Button, Entry, Frame, Label, Listbox, StringVar,
                     Text, Tk, Toplevel, OptionMenu, END)
from typing import Any, Dict, List, Tuple, Union, TypeVar, Callable
import copy
_parentType = Union[Frame, Toplevel, Tk]
from .dataClasses import ClassInfo


class ClassContentFrame(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        super().__init__(
            parent, background=self._settings["cnfs"]["general"]["background"])
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}

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
        self._classFrame = ClassInfoFrame(self, settings)
        self._membersFrame = MembersFrame(self, settings)
        self._methodsFrame = MethodsFrame(self, settings)

        self._placeElements()

    def _placeElements(self):
        self.rowconfigure(0, weight=1)
        for y in range(3):
            self.columnconfigure(y, weight=1)
        self._classFrame.grid(row=0, column=0, sticky="snew")
        self._membersFrame.grid(row=0, column=1, sticky="snew")
        self._methodsFrame.grid(row=0, column=2, sticky="snew")


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
        self._name: StringVar = self._frameElements["Name_EntryVar"]
        self._accessibility: StringVar = self._frameElements["Accesibility_OptionMenuVar"]
        self._extends: StringVar = self._frameElements["Extends_EntryVar"]
        self._description: Text = self._frameElements["Description_Text"]
        super()._lateInit()

    def setClassInfo(self, classInfo: ClassInfo):
        self._name = classInfo.getName()
        self._accessibility = classInfo.getAccessibility()
        self._extends = classInfo.getExtends()
        self._description.delete(1.0, END)
        self._description.insert(END, classInfo.getDescription())

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
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        super()._setFramesSequence([
            "Name:_Label",
            "Name_Entry",
            "Accessibility:_Label",
            "Accessibility_OptionMenu",
            "Type:_Label",
            "Type_Entry",
            "Empty_Label",
            "Description:_Label",
            "Description_Text",
            "Ok_OkButton",
            "Cancel_CancelButton"
        ])
        self._parent: _parentType = parent
        super()._lateInit()

    def _getOkButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._onOkButton)
        return button

    def _onOkButton(self) -> None:
        index: Union[str, int]
        try:
            index = self._membersList.curselection()[0] + 1
        except IndexError:
            index = END
        self._membersList.insert(index, f"VALUE {self.i}")
        self.i += 1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._parent.destroy)
        return button

    def _placeWidgets(self) -> None:
        elementsFound = super()._updateFrameElements()[0]
        for x in range(len(elementsFound)-1):
            self.rowconfigure(x, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        row = 0
        for element in elementsFound:
            if element == "Ok_OkButton":
                self._frameElements[element].grid(
                    row=row, column=0, sticky="snew")
            elif element == "Cancel_CancelButton":
                self._frameElements[element].grid(
                    row=row, column=1, sticky="snew")
                row += 1
            else:
                self._frameElements[element].grid(
                    row=row, column=0, sticky="snew")
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
        self._membersList: EnhListbox = self._frameElements["members_MembersListbox"]

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
            index = self._membersList.curselection()[0] + 1
        except IndexError:
            index = END
        self._membersList.insert(index, f"VALUE {self.i}")
        self.i += 1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("RemoveButton")
        cnf["command"] = self._onRemoveButton
        button.configure(cnf)
        return button

    def _onRemoveButton(self) -> None:
        try:
            index: int = self._membersList.curselection()[0]
            self._membersList.delete(index)
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
