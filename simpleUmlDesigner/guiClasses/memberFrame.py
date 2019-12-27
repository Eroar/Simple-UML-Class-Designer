from __future__ import annotations

from tkinter import Button, END
from typing import Any, Dict, Union

from .classContentFrame import ClassContentFrame, _parentType


class MemberFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        super()._setFramesSequence([
            "Name:_Label",
            "Name_Entry",
            "Accessibility:_Label",
            "Accessibility_OptionMenu",
            "Type:_Label",
            "Type_Entry",
            "Empty_Label",
            "Description:_Label",
            "Description_Text",
            "Ok_OkButton",
            "Cancel_CancelButton"
        ])
        self._parent: _parentType = parent
        super()._lateInit()

    def _getOkButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._onOkButton)
        return button

    def _onOkButton(self) -> None:
        index: Union[str, int]
        try:
            index = self._membersList.curselection()[0] + 1
        except IndexError:
            index = END
        self._membersList.insert(index, f"VALUE {self.i}")
        self.i += 1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        button.configure(command=self._parent.destroy)
        return button

    def _placeWidgets(self) -> None:
        elementsFound = super()._updateFrameElements()[0]
        for x in range(len(elementsFound)-1):
            self.rowconfigure(x, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        row = 0
        for element in elementsFound:
            if element == "Ok_OkButton":
                self._frameElements[element].grid(
                    row=row, column=0, sticky="snew")
            elif element == "Cancel_CancelButton":
                self._frameElements[element].grid(
                    row=row, column=1, sticky="snew")
                row+=1
            else:
                self._frameElements[element].grid(
                    row=row, column=0, sticky="snew")
                row += 1
