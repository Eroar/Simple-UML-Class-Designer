from __future__ import annotations

from tkinter import (BROWSE, Button, Entry, Frame, Label, Listbox, StringVar,
                     Text, Tk, Toplevel, OptionMenu)
from typing import Any, Dict, List, Tuple, Union, TypeVar

_parentType = Union[Frame, Toplevel, Tk]


class ClassContentFrame(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        super().__init__(parent, background=self._getSetting("background"))
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}
    
    def _setFramesSequence(self, newSequence: List[str]) ->None:
        self._frameElementsSequence = newSequence
    
    def _lateInit(self) -> None:
        #places all elements on frame
        self._placeWidgets()

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getSetting(self, setting: str) -> Any:
        return self._settings[setting]

    def _getLabel(self, text: str) -> Label:
        label: Label = Label(self, text=text, pady=5, font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))
        return label

    def _getEntry(self) -> Tuple[Entry, StringVar]:
        textVar: StringVar = StringVar(self)
        entry: Entry = Entry(self, textvariable=textVar, font=(self._getSetting("font"), self._getSetting("font-size")),
                             background=self._getSetting("field-background"), text="", justify="center")
        return entry, textVar

    def _getText(self) -> Text:
        text: Text = Text(self, font=(self._getSetting("font"), self._getSetting("font-size")),
                          background=self._getSetting("field-background"))
        return text

    def _getListBox(self) -> Listbox:
        listbox: Listbox = Listbox(self, selectmode=BROWSE, background=self._getSetting(
            "field-background"), width=self._getSetting("list-width"), height=self._getSetting("list-height"), bd=5, justify="center")
        listbox.configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")))
        return listbox

    def _getOptionMenu(self) -> OptionMenu:
        optionMenunVar: StringVar = StringVar(self)
        optionMenu: OptionMenu = OptionMenu(
            self, optionMenunVar, *self._getSetting("OptionMenu-values"))

        optionMenu.configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))

        optionMenu["menu"].configure(font=(self._getSetting("font"), self._getSetting(
            "font-size")), background=self._getSetting("background"))

        return optionMenu

    def _getButton(self) -> Button:
        button: Button = Button(self, font=(
            self._getSetting("font"), self._getSetting("font-size")))
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
                self._frameElements[key] = self._getEntry()[0]
            elif widget == "Text":
                self._frameElements[key] = self._getText()
            elif widget == "Listbox":
                self._frameElements[key] = self._getListBox()
            elif widget == "OptionMenu":
                self._frameElements[key] = self._getOptionMenu()
            else:
                elementsNotFound.append(key)
        elementsFound: List[str] = [
            element for element in self._frameElementsSequence if element not in elementsNotFound]
        return elementsFound, elementsNotFound

    def _placeWidgets(self) -> None:
        elementsFound = self._updateFrameElements()[0]
        for element in elementsFound:
            self._frameElements[element].pack(side="top")
