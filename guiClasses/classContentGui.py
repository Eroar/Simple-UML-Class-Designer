from __future__ import annotations

from abc import ABC
from tkinter import (SINGLE, Button, Entry, Frame, Label, Listbox, StringVar,
                     Text, Tk, Toplevel, OptionMenu)
from typing import Any, Dict, List, Tuple, Union


class ClassContentGui(ABC):
    def __init__(self, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str, Any] = {}

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getSetting(self, setting: str) -> Any:
        return self._settings[setting]

    def _getLabel(self, parent: Union[Frame, Toplevel, Tk], text: str) -> Label:
        # settings configurations:
        # label-font
        # label-font-size
        # label-background
        label: Label = Label(parent, text=text, pady=5, font=(self._getSetting("label-font"), self._getSetting(
            "label-font-size")), background=self._getSetting("label-background"))
        return label

    def _getEntry(self, parent: Union[Frame, Toplevel, Tk]) -> Tuple[Entry, StringVar]:
        # settings configurations:
        # entry-font
        # entry-font-size
        # entry-background
        textVar: StringVar = StringVar(parent)
        entry: Entry = Entry(parent, textvariable=textVar, font=(self._getSetting("entry-font"), self._getSetting("entry-font-size")),
                             background=self._getSetting("entry-background"), text="", justify="center")
        return entry, textVar

    def _getText(self, parent: Union[Frame, Toplevel, Tk], width: int, height: int) -> Text:
        # settings configurations:
        # text-font
        # text-font-size
        # text-background
        text: Text = Text(parent, font=(self._getSetting("text-font"), self._getSetting("text-font-size")),
                          background=self._getSetting("text-background"), width=width, height=height)
        return text

    def _getListBox(self, parent: Union[Frame, Toplevel, Tk], listSettingName: str = "normal") -> Listbox:
        # settings configurations:
        # -list-font
        # -list-font-size
        # -list-width
        # -list-height
        # -list-background

        sName: str = listSettingName
        listbox: Listbox = Listbox(self, selectmode=SINGLE, background=self._getSetting(
            sName+"-list-background"), width=self._getSetting(sName+"-list-width"), height=self._getSetting(sName+"-list-height"), bd=5)
        listbox.configure(font=(self._getSetting(sName+"-list-font"), self._getSetting(
            sName+"-list-font-size")))
        return listbox

    def _getOptionMenu(self, parent: Union[Frame, Toplevel, Tk]) -> OptionMenu:
        optionMenunVar: StringVar = StringVar(parent)
        optionMenu: OptionMenu = OptionMenu(
            parent, optionMenunVar, *self._getSetting("accessibility-types"))

        optionMenu.configure(font=(self._getSetting("text-font"), self._getSetting(
            "text-font-size")), background=self._getSetting("button-background"))

        optionMenu["menu"].configure(font=(self._getSetting("text-font"), self._getSetting(
            "text-font-size")), background=self._getSetting("button-background"))

        return optionMenu

    def _updateFrameElements(self, parent: Union[Frame, Toplevel, Tk]) -> Tuple[List[str], List[str]]:
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
                self._frameElements[key] = self._getText(
                    parent, int(keySplitted[1]), int(keySplitted[2]))
            elif widget == "Listbox":
                if len(keySplitted) != 3:
                    raise Exception(
                        "ListBox element should contain 3 elements")
                self._frameElements[key] = self._getListBox(
                    parent, keySplitted[1])
            elif widget == "OptionMenu":
                self._frameElements[key] = self._getOptionMenu(parent)
            else:
                elementsNotFound.append(key)
        elementsFound: List[str] = [
            element for element in self._frameElementsSequence if element not in elementsNotFound]
        return elementsFound, elementsNotFound

    def getFrame(self, parent: Union[Frame, Toplevel, Tk]) -> Frame:
        newFrame = Frame(parent, background = self._getSetting("background"))
        elementsFound = self._updateFrameElements(newFrame)[0]
        for element in elementsFound:
            self._frameElements[element].pack(side="top")
        return newFrame
