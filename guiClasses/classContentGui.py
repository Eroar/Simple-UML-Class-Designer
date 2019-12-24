from __future__ import annotations

from tkinter import Frame, Label, Entry, Text, Button, Toplevel, StringVar, Listbox
from typing import Union, Dict, Any, List, Tuple


class ClassContentGui:
    def __init__(self, settings: Dict[str, Any]):
        self._settings: Dict[str, Any] = settings
        self._frameElementsSequence: List[str] = []
        self._frameElements: Dict[str,Any] = {}

    def updateSettings(self, settings: Dict[str, Any]) -> None:
        self._settings = settings

    def _getSetting(self, setting: str) -> Any:
        return self._settings[setting]

    def _getLabel(self, parent:Union[Frame, Toplevel], text: str) -> Label:
        label: Label = Label(parent, text=text, pady=5, font=(self._getSetting("text-font"), self._getSetting(
            "text-font-size")), background=self._getSetting("background")).grid(row=2, column=0, sticky="wnes")
        return label

    def _getEntry(self, parent:Union[Frame, Toplevel]) -> Tuple[Entry, StringVar]:
        textVar: StringVar = StringVar(parent)
        entry: Entry = Entry(parent, textvariable=textVar, font=(self._getSetting("text-font"), self._getSetting("text-font-size")),
                             background=self._getSetting("button-background"), text="", justify="center")
        return entry, textVar

    def _getText(self, parent:Union[Frame, Toplevel], width:int, height:int) -> Text:
        text: Text = Text(parent, font=(self._getSetting("text-font"), self._getSetting("text-font-size")),
                          background=self._getSetting("description-background"), width=width, height=height)
        return text
    
    def _getList(self, parent:Union[Frame, Toplevel]) ->Listbox:
        pass
    def _updateFrameElements(self, parent:Union[Frame, Toplevel]) -> List[str]:
        self._frameElements = {}
        elementsNotFound:List[str]=[]
        for key in self._frameElementsSequence:
            keySplitted = key.split("_")
            name:str = keySplitted[0]
            widget:str = keySplitted[-1]

            if widget == "Label":
                if len(keySplitted)==3:
                    if keySplitted[1] == "Empty":
                        self._frameElements[name] = self._getLabel(parent, "")
                else:
                    self._frameElements[name] = self._getLabel(parent, name)
            elif widget == "Empty":
                self._frameElements[name] = self._getLabel(parent, name)
            elif widget=="Entry":
                self._frameElements[name] = self._getEntry(parent)[0]
            elif widget=="Text":
                self._frameElements[name] = self._getText(parent, int(keySplitted[1]), int(keySplitted[2]))
            elif widget=="Listbox":
                self._frameElements[name] = self._getEntry(parent)
        return elementsNotFound
            

    def getFrame(self, parent:Union[Frame, Toplevel])->Frame:

        newFrame = Frame(parent)
        for element in self._frameElements:
            pass
        return newFrame