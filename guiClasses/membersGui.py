from __future__ import annotations

from tkinter import Frame, Tk, Toplevel, Listbox, Button
from typing import Any, Dict, List, Tuple, Union, TypeVar

from .classContentGui import ClassContentGui


class MembersGui(ClassContentGui):
    def __init__(self, parent: Union[Frame, Toplevel, Tk], settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._frameElementsSequence: List[str] = [
            "addMember_AddButton",
            "removeMember_RemoveButton",
            "members_Listbox"
        ]

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(background=super()._getSetting(
            "AddButton-background"), command=self._onAddButton)
        return button

    def _onAddButton(self):
        pass

    def insertStuff(self) -> None:
        l = self._frameElements["members_Listbox"]
        for i in range(10):
            l.insert(i, f"TEST STRING {i}")

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(background=super()._getSetting(
            "RemoveButton-background"), command=self._onRemoveButton)
        return button

    def _onRemoveButton(self):
        pass

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        for key in elementsNotFound:
            if key == "addMember_AddButton":
                self._frameElements[key] = self._getAddButton()
            elif key == "removeMember_RemoveButton":
                self._frameElements[key] = self._getRemoveButton()

        return elementsFound, elementsNotFound

    def getFrame(self) -> Frame:
        newFrame = Frame(
            self._parent, background=super()._getSetting("background"))
        elementsFound, elementsNotFound = super()._updateFrameElements()

        for element in elementsFound:
            if element == "addMember_AddButton":
                self._frameElements[element].grid(
                    row=0, column=0, sticky="nesw")
            elif element == "removeMember_RemoveButton":
                self._frameElements[element].grid(
                    row=0, column=1, sticky="nesw")
            else:
                self._frameElements[element].grid(
                    row=1, column=0, sticky="nesw", columnspan=2)

        return newFrame
