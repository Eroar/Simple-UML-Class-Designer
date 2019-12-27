from __future__ import annotations

import copy
from abc import ABC
from typing import Any, Dict, List
import json


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


class ClassInfo(ClassContent):
    def __init__(self, name: str, accessibility: str = "", extends: str = "", description: str = ""):
        super().__init__(name, accessibility, description)
        self._extends = extends

    def setExtends(self, newExtend: str) -> None:
        self._extends = newExtend

    def getExtends(self) -> str:
        return self._extends


class Diagram(ClassContent):
    def __init__(self, name: str = "", accessibility: str = "", description: str = ""):
        self._classInfo: ClassInfo = ClassInfo(
            name, accessibility, description)
        self._members: List[Member] = []
        self._methods: List[Method] = []

    def addMember(self, member: Member):
        self._members.append(member)

    def setMember(self, index: int, newMember: Member) -> None:
        if index < len(self._members):
            self._members[index] = newMember

    def setMembers(self, newMembers: List[Member]) -> None:
        self._members = newMembers

    def removeMember(self, memberIndex: int) -> None:
        del self._members[memberIndex]

    def addMethod(self, method: Method):
        self._methods.append(method)

    def setMethod(self, index: int, newMethod: Method) -> None:
        if index < len(self._methods):
            self._methods[index] = newMethod

    def setMethods(self, newMethods: List[Method]) -> None:
        self._methods = newMethods

    def removeMethod(self, methodIndex: int) -> None:
        del self._methods[methodIndex]

    def getMembers(self) -> List[Member]:
        membersCopy = []

        for member in self._members:
            membersCopy.append(copy.copy(member))

        return membersCopy

    def getMethods(self) -> List[Method]:
        methodsCopy = []

        for method in self._methods:
            methodsCopy.append(copy.copy(method))
        return methodsCopy

    def getCopy(self) -> Diagram:
        return copy.copy(self)

    @staticmethod
    def diagramFromJson(jsonFilePath: str) -> Diagram:
        jDict: dict = {}
        with open(jsonFilePath, "r") as file:
            jDict = json.load(file)

        diagName: str = jDict["Class-Name"]
        newDiag: Diagram = Diagram(diagName)

        for memberDict in jDict["Members"]:
            newDiag.addMember(Member.memberFromDict(memberDict))

        for methodDict in jDict["Methods"]:
            newDiag.addMethod(Method.methodFromDict(methodDict))
        return newDiag

    @staticmethod
    def diagramFromDict(diagramDict: Dict["str", Any]) -> Diagram:

        newDiag: Diagram = Diagram(
            diagramDict["Class-Name"], diagramDict["Accessibility"], diagramDict["Description"])

        for memberDict in diagramDict["Members"]:
            newDiag.addMember(Member.memberFromDict(memberDict))

        for methodDict in diagramDict["Methods"]:
            newDiag.addMethod(Method.methodFromDict(methodDict))
        return newDiag

    def getDict(self) -> Dict["str", Any]:
        outDict: Dict[str, Any] = super().getDict()
        outDict["Members"] = []
        outDict["Methods"] = []

        for member in self._members:
            outDict["Members"].append(member.getDict())

        for method in self._methods:
            outDict["Methods"].append(method.getDict())
        return outDict

    def getDiagramJsons(self) -> str:
        return json.dumps(self.getDict())


class Member(ClassContent):
    def __init__(self, name: str, accessibility: str = "public", description: str = ""):
        super().__init__(name, accessibility, description)

    @staticmethod
    def memberFromDict(memberDict: dict) -> Member:
        name: str = memberDict["Name"]
        memberType: str = memberDict["Accessibility"]
        description: str = memberDict["Description"]
        return Member(name, memberType, description)


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
