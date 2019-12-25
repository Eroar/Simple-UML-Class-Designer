from __future__ import annotations

from tkinter import Frame, Tk, Toplevel
from typing import Any, Dict, List, Tuple, Union, TypeVar

from .classContentGui import ClassContentGui


class ClassGui(ClassContentGui):
    def __init__(self, parent:Union[Frame, Toplevel, Tk], settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._frameElementsSequence: List[str] = [
            "Accessibility:_Label",
            "Accesibility_OptionMenu",
            "Name:_Label",
            "Name_Entry",
            "Extends:_Label",
            "Extends_Entry",
            "Empty_Label",
            "Description:_Label",
            "Description_Text"
        ]

    def getFrame(self) -> Frame:
        newFrame = Frame(self._parent, background=super()._getSetting("background"))
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
        return newFrame
