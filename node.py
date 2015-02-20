class Connector:
	def __init__(self,owner, name, activates=0, monitor=0):
		self.value = None
		self.owner = owner
		self.name = name
		self.monitor = monitor
		self.connects = []
		self.activates = activates


	def connect(self, inputs):
		if type(inputs) != type([]):
			inputs = [inputs]
		for input in inputs:
			self.connects.append(input)

	def set(self, value):
		if self.value == value:
			return

		self.value = value

		if self.activates:
			self.owner.evaluate()

		for con in self.connects:
			con.set(value)


class LC:
	def __init__(self, name = "temp"):
		self.name = name

	def evaluate():
		return


class Not(LC):
	def __init__(self, name):
		LC.__init__(self, name)
		self.input1 = Connector(self,'A', activates=1)
		self.output = Connector(self,'B')

	def evaluate(self):
		self.output.set(not self.input1.value)

class Gate2(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.input1 = Connector(self, 'A', activates = 1)
		self.input2 = Connector(self, 'B', activates = 1)
		self.output = Connector(self, 'C')


class And(Gate2):
	def __init__(self, name):
		Gate2.__init__(self, name)

	def evaluate(self):
		self.output.set(self.input1.value and self.input2.value)

class Or(Gate2):
	def __init__(self, name):
		Gate2.__init__(self, name)

	def evaluate(self):
		self.output.set(self.input1.value or self.input2.value)

class Xor(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        self.A1 = And("A1")   # See circuit drawing to follow connections
        self.A2 = And("A2")
        self.I1 = Not("I1")
        self.I2 = Not("I2")
        self.O1 = Or("O1")
        self.A.connect([self.A1.A, self.I2.A])
        self.B.connect([self.I1.A, self.A2.A])
        self.I1.B.connect([self.A1.B ])
        self.I2.B.connect([self.A2.B ])
        self.A1.C.connect([self.O1.A ])
        self.A2.C.connect([self.O1.B ])
        self.O1.C.connect([self.C ])

class HalfAdder(LC):          # One bit adder, A,B in. Sum and Carry out
    def __init__(self, name):
        LC.__init__(self, name)
        self.A = Connector(self, 'A', 1)
        self.B = Connector(self, 'B', 1)
        self.S = Connector(self, 'S')
        self.C = Connector(self,'C')
        self.X1= Xor("X1")
        self.A1= And("A1")
        self.A.connect([self.X1.A, self.A1.A])
        self.B.connect([self.X1.B, self.A1.B])
        self.X1.C.connect([self.S])
        self.A1.C.connect([self.C])

class FullAdder(LC):          # One bit adder, A,B,Cin in. Sum and Cout out
    def __init__(self, name):
        LC.__init__(self, name)
        self.A = Connector(self, 'A', 1, monitor=1)
        self.B = Connector(self, 'B', 1, monitor=1)
        self.Cin = Connector(self, 'Cin', 1, monitor=1)
        self.S = Connector(self, 'S', monitor=1)
        self.Cout = Connector(self, 'Cout', monitor=1)
        self.H1 = HalfAdder("H1")
        self.H2 = HalfAdder("H2")
        self.O1 = Or("O1")
        self.A.connect([self.H1.A ])
        self.B.connect([self.H1.B ])
        self.Cin.connect([self.H2.A ])
        self.H1.S.connect([self.H2.B ])
        self.H1.C.connect([self.O1.B])
        self.H2.C.connect([self.O1.A])
        self.H2.S.connect([self.S])
        self.O1.C.connect([self.Cout])
