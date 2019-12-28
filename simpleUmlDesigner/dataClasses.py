from __future__ import annotations

import copy
from abc import ABC
from typing import Any, Dict, List, Optional, cast
import json
from os import listdir
from os.path import isfile, join


class Content(ABC):
    _defaultCnf: Dict[str, Any] = {
        "name": "",
        "accessibility": "",
        "description": ""
    }

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        self._name: str = cnf["name"]
        self._accessibility: str = cnf["accessibility"]
        self._describtion: str = cnf["description"]

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

    def getCopy(self) -> Content:
        return copy.deepcopy(self)

    def getDict(self) -> Dict[str, str]:
        outDict: Dict[str, str] = {
            "name": self._name,
            "accessibility": self._accessibility,
            "description": self._describtion
        }
        return outDict

    @staticmethod
    def fromDict(cnf: dict) -> Content:
        return Content(cnf)


class ClassInfo(Content):
    _defaultCnf: Dict[str, Any] = Content._defaultCnf
    _defaultCnf["extends"] = ""

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)
        self._extends = cnf["extends"]

    def setExtends(self, newExtend: str) -> None:
        self._extends = newExtend

    def getExtends(self) -> str:
        return self._extends

    def getDict(self):
        outDict: Dict[str, Any] = super().getDict()
        outDict["extends"] = self._extends
        return outDict

    @staticmethod
    def fromDict(cnf: dict) -> ClassInfo:
        return ClassInfo(cnf)


class TypeContent(Content):
    _defaultCnf: Dict[str, Any] = Content._defaultCnf
    _defaultCnf["type"] = ""

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)
        self._type = cnf["type"]

    def setType(self, newType: str) -> None:
        self._type = newType

    def getType(self) -> str:
        return self._type

    def getDict(self):
        outDict: Dict[str, Any] = super().getDict()
        outDict["type"] = self._type
        return outDict

    @staticmethod
    def fromDict(cnf: dict) -> TypeContent:
        return TypeContent(cnf)


class Method(TypeContent):
    _defaultCnf: Dict[str, Any] = TypeContent._defaultCnf
    _defaultCnf["inputs"] = []

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)
        self._inputs: List[Input] = cnf["inputs"]

    def setInputs(self, newInputs: List[Input]) -> None:
        self._inputs = newInputs

    def getInputs(self) -> List[Input]:
        return self._inputs

    def _getInputsListOfDicts(self) -> List[Dict[str, str]]:
        outList: List[Dict[str, str]] = []
        for inpt in self._inputs:
            outList.append(inpt.getDict())
        return outList

    def getDict(self) -> Dict[str, Any]:
        outDict: Dict[str, Any] = super().getDict()
        outDict["Inputs"] = self._getInputsListOfDicts()
        return outDict

    @staticmethod
    def _getInputsFromListOfDicts(lOfDicts: List[Dict[str, str]]) -> List[Input]:
        outList: List[Input] = []
        for dic in lOfDicts:
            outList.append(Input.fromDict(dic))
        return outList

    @staticmethod
    def fromDict(cnf: dict) -> Method:
        inputs: List[Input] = Method._getInputsFromListOfDicts(
            cnf["Inputs"])
        return Method(cnf, inputs=inputs)


class DefaultTypeContent(TypeContent):
    _defaultCnf: Dict[str, Any] = Content._defaultCnf
    _defaultCnf["defaultValue"] = ""

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)
        self._defaulValue = cnf["defaultValue"]

    def setDefaulValue(self, newDefaultVaule: str) -> None:
        self._defaulValue = newDefaultVaule

    def getDefaulValue(self) -> str:
        return self._defaulValue

    def getDict(self) -> Dict[str, Any]:
        outDict: Dict[str, Any] = super().getDict()
        outDict["DefaultValue"] = self._defaulValue
        return outDict

    @staticmethod
    def fromDict(cnf: dict) -> DefaultTypeContent:
        return DefaultTypeContent(cnf)


class Member(DefaultTypeContent):
    _defaultCnf: Dict[str, Any] = DefaultTypeContent._defaultCnf

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)

    def getStr(self):
        a: str = self.getAccessibility()
        n: str = self.getName()
        t: str = self.getType()
        return a + " " + n + ": " + t

    @staticmethod
    def fromDict(cnf: dict) -> Member:
        return Member(cnf)


class Input(DefaultTypeContent):
    _defaultCnf: Dict[str, Any] = DefaultTypeContent._defaultCnf

    def __init__(self, cnf=_defaultCnf, **kw):
        cnf = {**cnf, **kw}
        super().__init__(cnf)

    def getAccessibility(self):

        raise Exception("Input does not have access to accesibility")

    def setAccessibility(self):
        raise Exception("Input does not have access to accesibility")

    @staticmethod
    def fromDict(cnf: dict) -> Input:
        cnf["accessibility"] = ""
        return Input(cnf)


class Diagram:
    def __init__(self, name: str):
        self._classInfo: ClassInfo = ClassInfo(name=name)
        self._members: List[Member] = []
        self._methods: List[Method] = []

    def setClassInfo(self, newClassInfo: ClassInfo) -> None:
        self._classInfo = newClassInfo

    def getClassInfo(self) -> ClassInfo:
        return self._classInfo

    def addMember(self, member: Member) -> None:
        self._members.append(member)

    def setMember(self, index: int, newMember: Member) -> None:
        if index < len(self._members):
            self._members[index] = newMember

    def removeMember(self, memberIndex: int) -> None:
        del self._members[memberIndex]

    def setMembers(self, newMembers: List[Member]) -> None:
        self._members = newMembers

    def getMembers(self) -> List[Member]:
        membersCopy = []

        for member in self._members:
            membersCopy.append(copy.copy(member))

        return membersCopy

    def addMethod(self, method: Method) -> None:
        self._methods.append(method)

    def setMethod(self, index: int, newMethod: Method) -> None:
        if index < len(self._methods):
            self._methods[index] = newMethod

    def removeMethod(self, methodIndex: int) -> None:
        del self._methods[methodIndex]

    def setMethods(self, newMethods: List[Method]) -> None:
        self._methods = newMethods

    def getMethods(self) -> List[Method]:
        methodsCopy = []

        for method in self._methods:
            methodsCopy.append(copy.copy(method))
        return methodsCopy

    def getCopy(self) -> Diagram:
        return copy.copy(self)

    @staticmethod
    def fromJsonS(jsonString: str) -> Diagram:
        jDict: dict = json.loads(jsonString)

        return Diagram.fromDict(jDict)

    @staticmethod
    def fromDict(diagDict: Dict[str, Any]):
        classInfo: ClassInfo = ClassInfo.fromDict(diagDict["ClassInfo"])
        newDiag: Diagram = Diagram.fromClassInfo(classInfo)

        for memberDict in diagDict["Members"]:
            newDiag.addMember(Member.fromDict(memberDict))

        for methodDict in diagDict["Methods"]:
            newDiag.addMethod(Method.fromDict(methodDict))
        return newDiag

    @staticmethod
    def fromClassInfo(classInfo: ClassInfo) -> Diagram:
        newDiag: Diagram = Diagram(classInfo.getName())
        newDiag.setClassInfo(classInfo)

        return newDiag

    def getDict(self) -> Dict["str", Any]:
        outDict: Dict[str, Any] = {}
        outDict["ClassInfo"] = self._classInfo.getDict()
        outDict["Members"] = []
        outDict["Methods"] = []

        for member in self._members:
            outDict["Members"].append(member.getDict())

        for method in self._methods:
            outDict["Methods"].append(method.getDict())
        return outDict

    def getDiagramJsons(self) -> str:
        return json.dumps(self.getDict())


class DiagramsManager:
    def __init__(self, folderPath: str):
        self._folderPath: str = folderPath
        self._diagrams: List[Diagram] = []
        self._loadDiagrams
        self._originalDiagramIndex: Optional[int] = None
        self._editedDiagram: Optional[Diagram] = None

    def getDiagrams(self):
        return self._diagrams

    def _loadDiagrams(self) -> None:
        filesInFolder: List[str] = [f for f in listdir(
            self._folderPath) if isfile(join(self._folderPath, f))]

        self._diagrams = []
        for file in filesInFolder:
            with open(join(self._folderPath, file), "r") as f:
                diagDict = json.load(f)
            if self._isDictDiagram(diagDict):
                self._diagrams.append(Diagram.fromDict(diagDict))

    def _isDictDiagram(self, diagDict: Dict[str, str]) -> bool:
        try:
            keys2Check = ["ClassInfo", "Members", "Methods"]

            for key in keys2Check:
                if key not in diagDict:
                    return False
            return True
        except KeyError:
            return False

    def addDiagram(self, name: str) -> None:
        self._diagrams.append(Diagram(name))

    def removeDiagram(self, name: Optional[str] = None, index: Optional[int] = None) -> None:

        if name != None:
            for i, diag in enumerate(self._diagrams):
                if diag.getClassInfo().getName() == name:
                    del self._diagrams[i]

        elif index != None:
            del self._diagrams[cast(Any, index)]

        else:
            raise Exception("No name nor index provided")

    # def Edit


class EditingManager:
    def __init__(self):
        self._originalDiag: Diagram = None
        self._editDiag: Diagram = None

    def revertEditedDiagram(self) -> None:
        self._editDiag = self._originalDiag.getCopy()

    def setNewOriginalDiag(self, newDiag: Diagram) -> None:
        self._originalDiag = newDiag
        self._editDiag = newDiag.getCopy()

    def getDiag2Edit(self) -> Diagram:
        return self._editDiag
