from typing import Dict


class ClassContent:
    def __init__(self, name: str, accessibility: str, description: str):
        self._name: str = name
        self._accessibility: str = accessibility
        self._describtion: str = description

    def getName(self) -> str:
        return self._name

    def getAccessibility(self) -> str:
        return self._accessibility

    def getDescription(self) -> str:
        return self._describtion

    def getDict(self) -> Dict[str, str]:
        outDict: Dict[str, str] = {
            "Name": self._name,
            "Accessibility": self._accessibility,
            "Description": self._describtion
        }
        return outDict
