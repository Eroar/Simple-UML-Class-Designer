from __future__ import annotations

from typing import Any, Dict

from .classContentFrame import ClassContentFrame, _parentType

from ..dataClasses import ClassInfo

from tkinter import StringVar, Text, OptionMenu, END


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

    def setClassInfo(self, classInfo:ClassInfo):
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
