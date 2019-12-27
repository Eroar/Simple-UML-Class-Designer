from ..dataClasses.classInfoFrame import ClassInfoFrame
from ..dataClasses.membersFrame import MembersFrame
from ..dataClasses.methodsFrame import MethodsFrame
from .classContentFrame import _parentType
import json
from tkinter import Tk, Frame
from typing import Dict, List, Any

class ClassEditor(Frame):
    def __init__(self, parent: _parentType, settings: Dict[str, Any]):
        super().__init__(parent, background=settings["cnfs"]["general"]["background"])
        self._classFrame = ClassInfoFrame(self, settings)
        self._membersFrame = MembersFrame(self, settings)
        self._methodsFrame = MethodsFrame(self, settings)

        self._placeElements()

    def _placeElements(self):
        self.rowconfigure(0, weight=1)
        for y in range(3):
            self.columnconfigure(y, weight=1)
        self._classFrame.grid(row=0,column=0,sticky="snew")
        self._membersFrame.grid(row=0,column=1,sticky="snew")
        self._methodsFrame.grid(row=0,column=2,sticky="snew")
