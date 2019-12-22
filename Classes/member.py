from __future__ import annotations
from typing import Dict

class Member:
	def __init__(self, name: str, type: str, description: str):
		self._name: str = name
		self._type: str = type
		self._describtion: str = description
	
	def getName(self) -> str:
		return self._name
	
	def getType(self) -> str:
		return self._type
	
	def getDescription(self) -> str:
		return self._describtion

	def getDict(self) -> Dict[str, str]:
		outDict: Dict[str, str] = {
			"Name": self._name,
			"Type": self._type,
			"Description": self._describtion
		}
		return outDict
	
	@staticmethod
	def memberFromDict(memberDict: dict) -> Member:
		name: str = memberDict["Name"]
		memberType: str = memberDict["Type"]
		description: str = memberDict["Description"]
		return Member(name, memberType, description)
