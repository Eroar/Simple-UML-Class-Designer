class Animal:
	def __init__(self, name):
		self.name=name
	
	def sayName(self):
		print("I'm ", self.name)

class FourLeg(Animal):
	def __init__(self, name):
		super().__init__(name)
	
	def say(self):
		print("Im a fourleg")

class Dog(FourLeg):
	def __init__(self, name):
		super().__init__(name)
	
	def WoofAndSayName(self):
		print("Woof")
		super().sayName()
		super().say()

dog=Dog("reks")
dog.WoofAndSayName()