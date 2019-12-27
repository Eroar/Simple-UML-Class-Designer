from __future__ import annotations

import copy
from abc import ABC
from typing import Dict


class ClassContent(ABC):
    def __init__(self, name: str = "", accessibility: str = "", description: str = ""):
        self._name: str = name
        self._accessibility: str = accessibility
        self._describtion: str = description

    def setName(self, newName: str) -> None:
        self._name = newName

    def getName(self) -> str:
        return self._name

    def setAccessibility(self, newAccessibility: str) -> None:
        self._accessibility = newAccessibility

    def getAccessibility(self) -> str:
        return self._accessibility

    def setDescription(self, newDescription: str) -> None:
        self._describtion = newDescription

    def getDescription(self) -> str:
        return self._describtion

    def getCopy(self) -> ClassContent:
        return copy.deepcopy(self)

    def getDict(self) -> Dict[str, str]:
        outDict: Dict[str, str] = {
            "Name": self._name,
            "Accessibility": self._accessibility,
            "Description": self._describtion
        }
        return outDict
