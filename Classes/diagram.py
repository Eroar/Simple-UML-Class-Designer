from __future__ import annotations
from typing import List, Dict, Any
import json
import copy

from classContent import ClassContent
from member import Member
from method import Method

class Diagram(ClassContent):
	def __init__(self, name:str, accessibility:str="public", description:str=""):
		super().__init__(name, accessibility, description)
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
	def diagramFromJson(jsonFilePath : str) -> Diagram:
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

	def getDict(self) -> dict:
		outDict: Dict[str, Any] = super().getDict()
		outDict["Members"] = []
		outDict["Methods"] = []

		for member in self._members:
			outDict["Members"].append(member.getDict())

		for method in self._methods:
			outDict["Methods"].append(method.getDict())

		return outDict

	def getDiagramJson(self) -> str:
		return json.dumps(self.getDict())

if __name__ == "__main__":
	diag = Diagram("test")
	exampleMember = Member("var1", "int", "example description of it")
	diag.addMember(exampleMember)
	from pprint import pprint
	pprint(diag.getDict())