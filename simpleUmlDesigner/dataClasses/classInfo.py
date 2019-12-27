from .classContent import ClassContent


class ClassInfo(ClassContent):
    def __init__(self, name: str, accessibility: str = "", extends: str = "", description: str = ""):
        super().__init__(name, accessibility, description)
        self._extends = extends

    def setExtends(self, newExtend: str) -> None:
        self._extends = newExtend

    def getExtends(self) -> str:
        return self._extends
