from tkinter import Listbox, END
from .classContentFrame import _parentType
from typing import Dict, Any, Callable
import copy


class EnhListbox(Listbox):
    def __init__(self, master: _parentType, cnf: Dict[str, Any], onDoubleClick: Callable[[int], Any]):
        super().__init__(master, cnf)
        self._onDoubleClick: Callable[[int], Any] = onDoubleClick
        self._elementDragged: bool = False
        self._lastDraggingIndex: int = -1
        self._dragging: bool = False

        self.bind("<Double-Button-1>",
                  lambda event: self._onDoubleClickInternal())
        self._pickedElement: str = ""
        self.bind("<Button-3>",
                  lambda event: self._onRightClick(event))
        self.bind("<B3-Motion>",
                  lambda event: self._onDragging(event))
        self.bind("<ButtonRelease-3>",
                  lambda event: self._onRightRelease(event))

    def _getNearestIndex(self, y) -> int:
        index = self.nearest(y)
        if index == -1:
            index = 0
        return index

    def _onRightClick(self, event) -> None:
        index = self.nearest(event.y)
        if index != -1:
            self._dragging = True
            self.selection_clear(0, END)
            self.selection_set(index, index)
            self._pickedElement = copy.copy(self.get(index, index)[0])
            self._lastDraggingIndex = index

    def _onRightRelease(self, event) -> None:
        self._dragging = False

    def _onDragging(self, event) -> None:
        if self._dragging:
            index = self._getNearestIndex(event.y)
            if index != self._lastDraggingIndex:
                if self._lastDraggingIndex != -1:
                    self.delete(self._lastDraggingIndex,
                                self._lastDraggingIndex)
                index = self._getNearestIndex(event.y)

                if self.size() > 0:
                    if event.y > self.bbox(END)[1]+15:
                        index += 1
                self.insert(index, self._pickedElement)
                self.selection_clear(0, END)
                self.selection_set(index, index)
                self._lastDraggingIndex = index

    def _onDoubleClickInternal(self) -> None:
        try:
            index = self.curselection()[0]
        except IndexError:
            return
        self._onDoubleClick(index)
