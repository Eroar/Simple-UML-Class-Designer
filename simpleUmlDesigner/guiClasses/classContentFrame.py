from __future__ import annotations

from tkinter import (BROWSE, Button, Entry, Frame, Label, Listbox, StringVar,
                     Text, Tk, Toplevel, OptionMenu)
from typing import Any, Dict, List, Tuple, Union, TypeVar

_parentType = Union[Frame, Toplevel, Tk]


class ClassContentFrame(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        super().__init__(parent, background=self._settings["cnfs"]["general"]["background"])
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}

    def _setFramesSequence(self, newSequence: List[str]) -> None:
        self._frameElementsSequence = newSequence

    def _lateInit(self) -> None:
        # places all elements on frame
        self._placeWidgets()

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getCnf(self, *cnfNames:str) -> Dict[str, Any]:
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
                self._frameElements[key], self._frameElements[key+"Var"] = self._getEntry()
            elif widget == "Text":
                self._frameElements[key] = self._getText()
            elif widget == "Listbox":
                self._frameElements[key] = self._getListBox()
            elif widget == "OptionMenu":
                self._frameElements[key], self._frameElements[key+"Var"] = self._getOptionMenu()
            else:
                elementsNotFound.append(key)
        elementsFound: List[str] = [
            element for element in self._frameElementsSequence if element not in elementsNotFound]
        return elementsFound, elementsNotFound

    def _placeWidgets(self) -> None:
        elementsFound = self._updateFrameElements()[0]
        for element in elementsFound:
            self._frameElements[element].pack(side="top")
