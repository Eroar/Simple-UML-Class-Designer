from __future__ import annotations

from tkinter import Frame, Tk, Toplevel, Listbox, Button, END
from typing import Any, Dict, List, Tuple, Union, TypeVar

from .classContentFrame import ClassContentFrame, _parentType


class MethodsFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._setFramesSequence([
            "addMember_AddButton",
            "removeMember_RemoveButton",
            "members_Listbox"
        ])
        super()._lateInit()
        self._membersList: Listbox = self._frameElements["members_Listbox"]

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(text="Add member", background=super()._getSetting(
            "AddButton-background"), command=self._onAddButton)
        return button

    def _onAddButton(self) -> None:
        try:
            selectedIndex: int = self._membersList.curselection()[0]
            self._membersList.insert(
                selectedIndex+1, f"TEST INSERT correct position")
        except IndexError:
            self._membersList.insert(END, f"TEST INSERTED AT END")

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(text="Remove member", background=super()._getSetting(
            "RemoveButton-background"), command=self._onRemoveButton)
        return button

    def _onRemoveButton(self) -> None:
        self._membersList.delete(self._membersList.curselection())

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        newElementsNotFound: List[str] = []
        for key in elementsNotFound:

            if key == "addMember_AddButton":
                self._frameElements[key] = self._getAddButton()
                elementsFound.append(key)
            elif key == "removeMember_RemoveButton":
                self._frameElements[key] = self._getRemoveButton()
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
            elif key == "members_Listbox":
                self._frameElements[key].grid(
                    row=1, column=0, sticky="nesw", columnspan=2)
