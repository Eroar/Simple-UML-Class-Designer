from typing import List
import json
import copy

from member import Member
from method import Method

class Diagram:
    def __init__(self, name:str):
        self._name: str = name
        self._members: List[Member] = []
        self._methods: List[Method] = []
    
    def addMember(self, member: Member):
        self._members.append(member)
    
    def removeMember(self, memberIndex: int) -> None:
        del self._members[memberIndex]

    def addMethod(self, method: Method):
        self._methods.append(method)
    
    def removeMethod(self, methodIndex: int) -> None:
        del self._methods[methodIndex]
    
    def getMembers(self) -> List[Member]:
        membersCopy = []

        for member in self._members():
            membersCopy.append(copy.copy(member))

        return membersCopy
    
    def getMethods(self) -> List[Method]:
        methodsCopy = []

        for method in self._methods():
            methodsCopy.append(copy.copy(method))
            
        return methodsCopy

    @staticmethod
    def diagramFromJson(jsonFilePath:str) -> Diagram:
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
    
    def __dict__(self) -> dict:
        outDict = {}
        outDict["Class-Name"] = self._name

        outDict["Members"]: List[dict] = []
        for member in self._members:
            outDict["Members"].append(member.__dict__())

        outDict["Methods"]: List[dict] = []
        for method in self._methods:
            outDict["Methods"].append(method.__dict__())

        return outDict
    
    def getDiagramJson(self) -> str:
        return json.dumps(self.__dict__())

if __name__ == "__main__":
    diag = Diagram("test")
    from pprint import pprint
    pprint(diag.getDiagramJson())