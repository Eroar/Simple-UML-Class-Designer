from __future__ import annotations
from typing import Dict

from .classContent import ClassContent

class Member(ClassContent):
	def __init__(self, name:str, accessibility:str="public", description:str=""):
		super().__init__(name, accessibility, description)

	@staticmethod
	def memberFromDict(memberDict: dict) -> Member:
		name: str = memberDict["Name"]
		memberType: str = memberDict["Accessibility"]
		description: str = memberDict["Description"]
		return Member(name, memberType, description)
