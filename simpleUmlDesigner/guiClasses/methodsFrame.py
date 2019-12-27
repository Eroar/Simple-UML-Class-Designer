from __future__ import annotations

from tkinter import Frame, Tk, Toplevel, Listbox, Button, END
from typing import Any, Dict, List, Tuple, Union, TypeVar

from .classContentFrame import ClassContentFrame,  _parentType
from .enhListbox import EnhListbox


class MethodsFrame(ClassContentFrame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, settings)
        self._setFramesSequence([
            "addMethod_AddButton",
            "removeMethod_RemoveButton",
            "methods_MethodsListbox"
        ])
        super()._lateInit()
        self._methodsList: EnhListbox = self._frameElements["methods_MethodsListbox"]

        # Testing
        self.i = 0

    def _getAddButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("AddButton")
        cnf["command"] = self._onAddButton
        button.configure(cnf)
        return button

    def _onAddButton(self) -> None:
        index: Union[str, int]
        try:
            index = self._methodsList.curselection()[0] + 1
        except IndexError:
            index = END
        self._methodsList.insert(index, f"VALUE {self.i}")
        self.i += 1

    def _getRemoveButton(self) -> Button:
        button: Button = super()._getButton()
        cnf: Dict[str, Any] = super()._getCnf("RemoveButton")
        cnf["command"] = self._onRemoveButton
        button.configure(cnf)
        return button

    def _onRemoveButton(self) -> None:
        try:
            index: int = self._methodsList.curselection()[0]
            self._methodsList.delete(index)
        except IndexError:
            pass

    def _getMethodsListbox(self) -> EnhListbox:
        cnf: Dict[str, Any] = super()._getCnf(
            "general", "field", "justify-center")
        methodsListbox: EnhListbox = EnhListbox(
            self, cnf, self._onMethodsListboxDoubleClick)
        return methodsListbox

    def _onMethodsListboxDoubleClick(self, index: int) -> None:
        print(f"Double click {index}")

    def _updateFrameElements(self) -> Tuple[List[str], List[str]]:
        elementsFound, elementsNotFound = super()._updateFrameElements()

        newElementsNotFound: List[str] = []
        for key in elementsNotFound:

            if key == "addMethod_AddButton":
                self._frameElements[key] = self._getAddButton()
                elementsFound.append(key)
            elif key == "removeMethod_RemoveButton":
                self._frameElements[key] = self._getRemoveButton()
            elif key == "methods_MethodsListbox":
                self._frameElements[key] = self._getMethodsListbox()
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
            if key == "addMethod_AddButton":
                self._frameElements[key].grid(
                    row=0, column=0, sticky="nesw")
            elif key == "removeMethod_RemoveButton":
                self._frameElements[key].grid(
                    row=0, column=1, sticky="nesw")
            elif key == "methods_MethodsListbox":
                self._frameElements[key].grid(
                    row=1, column=0, sticky="nesw", columnspan=2)
