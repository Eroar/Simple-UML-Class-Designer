from __future__ import annotations
from typing import Dict

from .classContent import ClassContent


class Method(ClassContent):
    def __init__(self, name: str, accessibility: str = "public", description: str = "", input: str = "", outputType: str = ""):
        super().__init__(name, accessibility, description)
        self._input: str = input
        self._outputType: str = outputType

    def getInput(self) -> str:
        return self._input

    def getOutputType(self) -> str:
        return self._outputType

    @staticmethod
    def methodFromDict(memberDict: dict) -> Method:
        name: str = memberDict["Name"]
        memberType: str = memberDict["Accessibility"]
        description: str = memberDict["Description"]
        return Method(name, memberType, description)
