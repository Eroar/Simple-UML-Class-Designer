from __future__ import annotations

from tkinter import Frame, Tk, Toplevel, Listbox, Button, END
from typing import Any, Dict, List, Tuple, Union, TypeVar

from .classContentFrame import ClassContentFrame,  _parentType
from .enhListbox import EnhListbox


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


        #Testing
        self.i=0

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(text="Add member", background=super()._getSetting(
            "AddButton-background"), command=self._onAddButton)
        return button

    def _onAddButton(self) -> None:
        index:Union[str, int]
        try:
            index = self._membersList.curselection()[0] + 1
        except IndexError:
            index = END
        self._membersList.insert(index, f"VALUE {self.i}")
        self.i+=1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(text="Remove member", background=super()._getSetting(
            "RemoveButton-background"), command=self._onRemoveButton)
        return button

    def _onRemoveButton(self) -> None:
        try:
            index:int= self._membersList.curselection()[0]
            self._membersList.delete(index)
        except IndexError:
            pass

    def _getMembersListbox(self) -> EnhListbox:
        membersListbox : EnhListbox =  EnhListbox(self, {}, self._onMembersListboxDoubleClick)
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
