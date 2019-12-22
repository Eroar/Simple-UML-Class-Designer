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
    
    @staticmethod
    def memberFromDict(memberDict: dict) -> Member:
        name: str = memberDict["Name"]
        type: str = memberDict["Type"]
        description: str = memberDict["Description"]
        return Member(name, type, description)