from __future__ import annotations

from abc import ABC
from tkinter import (SINGLE, Button, Entry, Frame, Label, Listbox, StringVar,
                     Text, Tk, Toplevel, OptionMenu)
from typing import Any, Dict, List, Tuple, Union, TypeVar

parentType = Union[Frame, Toplevel, Tk]


class ClassContentGui(ABC):
    def __init__(self, parent: parentType, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}
        self._parent: parentType = parent

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getSetting(self, setting: str) -> Any:
        return self._settings[setting]

    def _getLabel(self, parent: parentType, text: str) -> Label:
        label: Label = Label(parent, text=text, pady=5, font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))
        return label

    def _getEntry(self, parent: parentType) -> Tuple[Entry, StringVar]:
        textVar: StringVar = StringVar(parent)
        entry: Entry = Entry(parent, textvariable=textVar, font=(self._getSetting("font"), self._getSetting("font-size")),
                             background=self._getSetting("field-background"), text="", justify="center")
        return entry, textVar

    def _getText(self, parent: parentType) -> Text:
        text: Text = Text(parent, font=(self._getSetting("font"), self._getSetting("font-size")),
                          background=self._getSetting("field-background"))
        return text

    def _getListBox(self, parent: parentType) -> Listbox:
        listbox: Listbox = Listbox(parent, selectmode=SINGLE, background=self._getSetting(
            "field-background"), width=self._getSetting("list-width"), height=self._getSetting("list-height"), bd=5, justify="center")
        listbox.configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")))
        return listbox

    def _getOptionMenu(self, parent: parentType) -> OptionMenu:
        optionMenunVar: StringVar = StringVar(parent)
        optionMenu: OptionMenu = OptionMenu(
            parent, optionMenunVar, *self._getSetting("OptionMenu-values"))

        optionMenu.configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))

        optionMenu["menu"].configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))

        return optionMenu

    def _getButton(self, parent: parentType) -> Button:
        button: Button = Button(parent, font=(
            self._getSetting("font"), self._getSetting("font-size")))
        return button

    def _updateFrameElements(self, parent: parentType) -> Tuple[List[str], List[str]]:
        self._frameElements = {}
        elementsNotFound: List[str] = []
        for key in self._frameElementsSequence:
            keySplitted = key.split("_")
            name: str = keySplitted[0]
            widget: str = keySplitted[-1]

            if widget == "Label":
                if name == "Empty":
                    # Name_Empty_Label
                    self._frameElements[key] = self._getLabel(parent, "")
                else:
                    self._frameElements[key] = self._getLabel(parent, name)
            elif widget == "Entry":
                self._frameElements[key] = self._getEntry(parent)[0]
            elif widget == "Text":
                self._frameElements[key] = self._getText(parent)
            elif widget == "Listbox":
                self._frameElements[key] = self._getListBox(
                    parent)
            elif widget == "OptionMenu":
                self._frameElements[key] = self._getOptionMenu(parent)
            else:
                elementsNotFound.append(key)
        elementsFound: List[str] = [
            element for element in self._frameElementsSequence if element not in elementsNotFound]
        return elementsFound, elementsNotFound

    def getFrame(self, parent: parentType) -> Frame:
        newFrame = Frame(parent, background=self._getSetting("background"))
        elementsFound = self._updateFrameElements(newFrame)[0]
        for element in elementsFound:
            self._frameElements[element].pack(side="top")
        return newFrame
